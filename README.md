# ATEC Workspace

This repository is the lightweight code-sync workspace for ATEC simulation challenge work.

Large official bundles, videos, robot assets, datasets, checkpoints, simulator caches, and generated training outputs should stay out of Git. Use the remote GPU workspace for Isaac Lab setup, Task E data collection, training, evaluation, and log inspection.

Fixed workflow:

- Local workspace: `/Users/yangjc/Desktop/Sii/ATEC`
- GitHub repo: `YangJC112/atec_tmp`
- Remote workspace: `/inspire/hdd/project/multi-agent/yangjiachi-253108100068/ATEC`
- Remote helper skill: `/Users/yangjc/.codex/skills/atec-ssh`

## Task E Piper Baseline

The default Task E submission code is:

- `guide/ATEC2026_Simulation_Challenge/demo/solution.py`
- Environment id: `ATEC-TaskE-Piper`
- Robot config on the submission page: `Piper`

This checked-in version is the RGB-D geometry baseline that reached the verified
6-point run on the remote Isaac Lab machine. It uses the official camera/depth
observations to estimate object and basket positions, then runs a deterministic
pick-place state sequence for Piper. It does not depend on external model
weights, SAM API calls, or API keys.

To reproduce a local/remote evaluation from the challenge directory:

```bash
cd /inspire/hdd/project/multi-agent/yangjiachi-253108100068/ATEC/ATEC2026_Simulation_Challenge
PYTHON=/root/miniconda3/envs/isaaclab/bin/python scripts/run_task_e_piper_verified.sh
```

The wrapper sets the Isaac Sim EULA variables, pins the Task E/Piper task, uses
the verified seed `2`, and uses a temporary NVIDIA Vulkan/EGL ICD on machines
where the default Vulkan ICD does not work. Override the seed with:

```bash
ATEC_TASK_E_SEED=2 PYTHON=/root/miniconda3/envs/isaaclab/bin/python scripts/run_task_e_piper_verified.sh
```

If a future SAM API based variant is added, pass its key through an environment
variable such as `SAM_API_KEY`. Real API keys and tokens must not be committed to
this repository.
