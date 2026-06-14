#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
CHALLENGE_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
cd "$CHALLENGE_DIR"

PYTHON_BIN="${PYTHON:-python}"
TASK_SEED="${ATEC_TASK_E_SEED:-2}"
USE_TEMP_VULKAN_ICD="${ATEC_USE_TEMP_VULKAN_ICD:-1}"
TMP_DIR=""

cleanup() {
  if [ -n "${TMP_DIR:-}" ] && [ -d "$TMP_DIR" ]; then
    rm -rf "$TMP_DIR"
  fi
}
trap cleanup EXIT

export OMNI_KIT_ACCEPT_EULA="${OMNI_KIT_ACCEPT_EULA:-YES}"
export ACCEPT_EULA="${ACCEPT_EULA:-Y}"

if [ "$USE_TEMP_VULKAN_ICD" != "0" ]; then
  TMP_DIR="$(mktemp -d)"
  cat >"$TMP_DIR/nvidia_icd.json" <<'JSON'
{"file_format_version":"1.0.0","ICD":{"library_path":"libEGL_nvidia.so.0","api_version":"1.4.303"}}
JSON
  cat >"$TMP_DIR/10_nvidia.json" <<'JSON'
{"file_format_version":"1.0.0","ICD":{"library_path":"libEGL_nvidia.so.0"}}
JSON
  export VK_ICD_FILENAMES="$TMP_DIR/nvidia_icd.json"
  export __EGL_VENDOR_LIBRARY_FILENAMES="$TMP_DIR/10_nvidia.json"
fi

exec "$PYTHON_BIN" scripts/play_atec_task.py \
  --task ATEC-TaskE-Piper \
  --headless \
  --enable_cameras \
  --seed "$TASK_SEED" \
  "$@"
