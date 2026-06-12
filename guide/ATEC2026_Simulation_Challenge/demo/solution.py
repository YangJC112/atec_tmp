from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import torch


# Task-E scene constants from the official configuration.
TABLE_CENTER_X = 1.00
TABLE_CENTER_Y = 0.00
TABLE_DIMS_AT_0P008 = (0.6468062441005529, 0.9084968693231588, 0.6613141183247961)
TABLE_SCALE = 0.01
TABLE_DIMS = tuple(dim * (TABLE_SCALE / 0.008) for dim in TABLE_DIMS_AT_0P008)
TABLE_HALF_X = TABLE_DIMS[0] * 0.5
TABLE_TOP_Z = TABLE_DIMS[2]

ROOT_POS_W = np.array([TABLE_CENTER_X + TABLE_HALF_X, TABLE_CENTER_Y, TABLE_TOP_Z], dtype=np.float64)
BASKET_CENTER_W = np.array([TABLE_CENTER_X + 0.08, TABLE_CENTER_Y - 0.30, TABLE_TOP_Z + 0.16], dtype=np.float64)
CARRY_Z = TABLE_TOP_Z + 0.40
HOME_POS_W = np.array([TABLE_CENTER_X + TABLE_HALF_X - 0.10, TABLE_CENTER_Y, CARRY_Z], dtype=np.float64)

DEFAULT_JOINT_POS = np.array([0.0, 1.2, -1.5, 0.0, 1.2, 0.0, 0.035, -0.035], dtype=np.float64)
HOME_Q = np.array([-0.000033, 0.924525, -1.514983, 0.000011, 1.219900, -0.000033], dtype=np.float64)
GRIPPER_OPEN = np.array([0.035, -0.035], dtype=np.float64)
GRIPPER_CLOSED = np.array([-0.015, 0.015], dtype=np.float64)

JOINT_LIMITS = np.array(
    [
        [-154.0, 154.0],
        [0.0, 195.0],
        [-175.0, 0.0],
        [-102.0, 102.0],
        [-75.0, 75.0],
        [-120.0, 120.0],
    ],
    dtype=np.float64,
) * np.pi / 180.0

# Standard DH parameters [alpha, a, d, theta_offset] for AgileX Piper.
DH_PARAMS = np.array(
    [
        [-np.pi / 2, 0.0, 0.123, 0.0],
        [0.0, 0.28503, 0.0, -172.22 * np.pi / 180.0],
        [np.pi / 2, -0.021984, 0.0, -102.78 * np.pi / 180.0],
        [-np.pi / 2, 0.0, 0.25075, 0.0],
        [np.pi / 2, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.091, 0.0],
    ],
    dtype=np.float64,
)

# Fixed Task-E external RGB-D camera. Quaternion is CameraData.quat_w_ros (w, x, y, z).
CAM_POS_W = np.array([-0.20000000298023224, 0.0, TABLE_TOP_Z + 0.8], dtype=np.float64)
CAM_QUAT_W_ROS = np.array([-0.3335084915161133, 0.6235159635543823, -0.6235158443450928, 0.3335084915161133])
CAM_FX = 732.999267578125
CAM_FY = 732.999267578125
CAM_CX = 320.0
CAM_CY = 240.0

TARGET_CENTER_OFFSETS = {
    1: np.array([0.000, 0.000, 0.0], dtype=np.float64),
    2: np.array([0.000, 0.000, 0.0], dtype=np.float64),
    3: np.array([0.000, 0.000, 0.0], dtype=np.float64),
}


def _quat_to_matrix_wxyz(q: np.ndarray) -> np.ndarray:
    w, x, y, z = q.astype(np.float64)
    return np.array(
        [
            [1.0 - 2.0 * (y * y + z * z), 2.0 * (x * y - z * w), 2.0 * (x * z + y * w)],
            [2.0 * (x * y + z * w), 1.0 - 2.0 * (x * x + z * z), 2.0 * (y * z - x * w)],
            [2.0 * (x * z - y * w), 2.0 * (y * z + x * w), 1.0 - 2.0 * (x * x + y * y)],
        ],
        dtype=np.float64,
    )


CAM_R_WC = _quat_to_matrix_wxyz(CAM_QUAT_W_ROS)


def _dh_transform(alpha: float, a: float, d: float, theta: float) -> np.ndarray:
    c = np.cos(theta)
    s = np.sin(theta)
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    return np.array(
        [
            [c, -s * ca, s * sa, a * c],
            [s, c * ca, -c * sa, a * s],
            [0.0, sa, ca, d],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=np.float64,
    )


def _fk_piper_base(q6: np.ndarray) -> np.ndarray:
    transform = np.eye(4, dtype=np.float64)
    for q, (alpha, a, d, offset) in zip(q6, DH_PARAMS):
        transform = transform @ _dh_transform(float(alpha), float(a), float(d), float(q + offset))
    return transform[:3, 3]


def _fk_piper_transform(q6: np.ndarray) -> np.ndarray:
    transform = np.eye(4, dtype=np.float64)
    for q, (alpha, a, d, offset) in zip(q6, DH_PARAMS):
        transform = transform @ _dh_transform(float(alpha), float(a), float(d), float(q + offset))
    return transform


_S_DH_TO_WORLD = np.diag([-1.0, -1.0, 1.0])
_GRIPPER_ROT_W_Q_ZERO = _quat_to_matrix_wxyz(
    np.array([-4.828059445571853e-06, 0.6756134629249573, -2.1430751075968146e-06, -0.7372560501098633])
)
_LINK6_TO_GRIPPER_ROT = _fk_piper_transform(np.zeros(6, dtype=np.float64))[:3, :3].T @ _S_DH_TO_WORLD.T @ _GRIPPER_ROT_W_Q_ZERO
_TOP_DOWN_ROT_W = _quat_to_matrix_wxyz(np.array([0.0, 1.0, 0.0, 0.0], dtype=np.float64))
_GRASP_ROT_W_BY_OBJECT = {
    1: np.array(
        [
            [0.0, -1.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 0.0, -1.0],
        ],
        dtype=np.float64,
    ),
    2: np.array(
        [
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, -1.0],
        ],
        dtype=np.float64,
    ),
    3: np.array(
        [
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, -1.0],
        ],
        dtype=np.float64,
    ),
}


def _world_to_piper_base(pos_w: np.ndarray) -> np.ndarray:
    delta = pos_w - ROOT_POS_W
    return np.array([-delta[0], -delta[1], delta[2]], dtype=np.float64)


def _rot_error(current: np.ndarray, target: np.ndarray) -> np.ndarray:
    return 0.5 * (
        np.cross(current[:, 0], target[:, 0])
        + np.cross(current[:, 1], target[:, 1])
        + np.cross(current[:, 2], target[:, 2])
    )


def _pose_error(target_pos_base: np.ndarray, target_rot_w: np.ndarray, q: np.ndarray) -> np.ndarray:
    transform = _fk_piper_transform(q)
    pos_err = target_pos_base - transform[:3, 3]
    rot_w = _S_DH_TO_WORLD @ transform[:3, :3] @ _LINK6_TO_GRIPPER_ROT
    rot_err = _rot_error(rot_w, target_rot_w)
    return np.r_[pos_err, 0.35 * rot_err]


def _ik_position(
    target_w: np.ndarray,
    q_init: np.ndarray,
    target_rot_w: np.ndarray | None = None,
    max_iter: int = 70,
) -> np.ndarray:
    target = _world_to_piper_base(target_w)
    target_rot = _TOP_DOWN_ROT_W if target_rot_w is None else target_rot_w
    q = np.clip(q_init[:6].astype(np.float64), JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])
    q = 0.75 * q + 0.25 * HOME_Q

    for _ in range(max_iter):
        err = _pose_error(target, target_rot, q)
        if np.linalg.norm(err[:3]) < 0.008 and np.linalg.norm(err[3:]) < 0.025:
            break

        jac = np.zeros((6, 6), dtype=np.float64)
        eps = 1.0e-4
        for i in range(6):
            q_eps = q.copy()
            q_eps[i] += eps
            jac[:, i] = (_pose_error(target, target_rot, q_eps) - err) / eps

        damping = 0.07
        lhs = jac @ jac.T + (damping * damping) * np.eye(err.shape[0])
        delta = -jac.T @ np.linalg.solve(lhs, err)
        delta = np.clip(delta, -0.08, 0.08)
        q = np.clip(q + delta, JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])

    return q


def _as_numpy(value: Any) -> np.ndarray:
    if isinstance(value, torch.Tensor):
        return value.detach().cpu().numpy()
    return np.asarray(value)


@dataclass
class TargetObject:
    object_id: int
    pos_w: np.ndarray


@dataclass
class Stage:
    name: str
    pos_w: np.ndarray | None
    gripper: np.ndarray
    min_steps: int
    max_steps: int
    tolerance: float = 0.045


class AlgSolution:
    def __init__(self):
        self._targets: list[TargetObject] = []
        self._target_idx = 0
        self._stage_idx = 0
        self._stage_step = 0
        self._basket_pos_w = BASKET_CENTER_W.copy()
        self._stages: list[Stage] = []
        self._last_q_target = np.r_[HOME_Q, GRIPPER_OPEN]
        self._stage_q_cache: dict[tuple[int, int, str], np.ndarray] = {}
        self._grid_cache: dict[tuple[int, int, int], tuple[np.ndarray, np.ndarray]] = {}

    def reset(self, **_: Any) -> None:
        self.__init__()

    def get_action_spec(self) -> dict[str, dict[str, Any]] | None:
        return {}

    def predicts(self, obs, current_score):
        proprio = obs["proprio"]
        device = proprio.device if isinstance(proprio, torch.Tensor) else "cpu"
        q_abs = _as_numpy(proprio)[0, :8].astype(np.float64) + DEFAULT_JOINT_POS

        if not self._targets:
            self._targets = self._detect_targets(obs)
            self._basket_pos_w = self._detect_basket(obs)
            self._target_idx = 0
            self._stage_idx = 0
            self._stage_step = 0
            self._stages = self._build_stages(self._targets[0]) if self._targets else []

        if not self._stages:
            action = np.zeros((1, 8), dtype=np.float32)
            return {"action": action.tolist(), "giveup": False}

        stage = self._stages[self._stage_idx]
        q_cmd = self._command_for_stage(stage, q_abs)

        self._stage_step += 1
        if self._stage_done(stage, q_abs) and self._stage_idx < len(self._stages) - 1:
            self._stage_idx += 1
            self._stage_step = 0
        elif self._stage_done(stage, q_abs) and self._stage_idx == len(self._stages) - 1:
            self._target_idx += 1
            if self._target_idx < len(self._targets):
                self._stages = self._build_stages(self._targets[self._target_idx])
                self._stage_idx = 0
                self._stage_step = 0
            else:
                self._stages = [Stage("done", HOME_POS_W, GRIPPER_OPEN, 999999, 999999, 0.10)]
                self._stage_idx = 0
                self._stage_step = 0

        action = ((q_cmd - DEFAULT_JOINT_POS) / 0.5).astype(np.float32)
        return {"action": torch.as_tensor(action, dtype=torch.float32, device=device).view(1, 8).cpu().numpy().tolist(), "giveup": False}

    def _stage_done(self, stage: Stage, q_abs: np.ndarray) -> bool:
        if self._stage_step < stage.min_steps:
            return False
        if self._stage_step >= stage.max_steps:
            return True
        if stage.pos_w is None:
            return True
        ee_w = self._fk_world(q_abs[:6])
        return bool(np.linalg.norm(ee_w - stage.pos_w) <= stage.tolerance)

    def _command_for_stage(self, stage: Stage, q_abs: np.ndarray) -> np.ndarray:
        if stage.name == "home_joint":
            q6 = HOME_Q
        elif stage.pos_w is None:
            q6 = self._last_q_target[:6]
        else:
            cache_key = (self._target_idx, self._stage_idx, stage.name)
            if cache_key not in self._stage_q_cache:
                self._stage_q_cache[cache_key] = _ik_position(stage.pos_w, self._last_q_target[:6])
            q6 = self._stage_q_cache[cache_key]
            self._last_q_target[:6] = q6

        gripper = stage.gripper
        q_target = np.r_[q6, gripper]
        max_delta = np.array([0.075, 0.075, 0.075, 0.10, 0.10, 0.12, 0.018, 0.018], dtype=np.float64)
        q_cmd = q_abs + np.clip(q_target - q_abs, -max_delta, max_delta)
        self._last_q_target = q_target
        return q_cmd

    def _build_stages(self, target: TargetObject) -> list[Stage]:
        x, y, z = target.pos_w.tolist()
        grasp_offset = {1: 0.055, 2: 0.070, 3: 0.050}.get(target.object_id, 0.055)
        grasp_z = float(np.clip(z + grasp_offset, TABLE_TOP_Z + 0.095, TABLE_TOP_Z + 0.20))
        pre = np.array([x, y, CARRY_Z], dtype=np.float64)
        reach = np.array([x, y, grasp_z], dtype=np.float64)
        lift = np.array([x, y, CARRY_Z], dtype=np.float64)
        basket_high = np.array([self._basket_pos_w[0], self._basket_pos_w[1], CARRY_Z], dtype=np.float64)
        basket_place = np.array([self._basket_pos_w[0], self._basket_pos_w[1], TABLE_TOP_Z + 0.15], dtype=np.float64)
        return [
            Stage("home_joint", None, GRIPPER_OPEN, 50, 90, 0.12),
            Stage("pre", pre, GRIPPER_OPEN, 35, 150),
            Stage("reach", reach, GRIPPER_OPEN, 35, 150),
            Stage("close", reach, GRIPPER_CLOSED, 38, 55, 0.06),
            Stage("lift", lift, GRIPPER_CLOSED, 45, 150),
            Stage("basket_high", basket_high, GRIPPER_CLOSED, 45, 180),
            Stage("basket_place", basket_place, GRIPPER_CLOSED, 35, 140),
            Stage("open", basket_place, GRIPPER_OPEN, 45, 65, 0.06),
            Stage("retract", HOME_POS_W, GRIPPER_OPEN, 35, 120, 0.07),
        ]

    def _fk_world(self, q6: np.ndarray) -> np.ndarray:
        p = _fk_piper_base(q6)
        return ROOT_POS_W + np.array([-p[0], -p[1], p[2]], dtype=np.float64)

    def _detect_targets(self, obs) -> list[TargetObject]:
        image = obs.get("image", {})
        if "video_depth" not in image or image["video_depth"] is None:
            return self._fallback_targets()

        depth = _as_numpy(image["video_depth"])
        if depth.ndim == 4:
            depth = depth[0, :, :, 0]
        elif depth.ndim == 3:
            depth = depth[0] if depth.shape[0] == 1 else depth[:, :, 0]
        depth = depth.astype(np.float64)

        h, w = depth.shape
        stride = 3
        cache_key = (h, w, stride)
        if cache_key not in self._grid_cache:
            vv, uu = np.mgrid[0:h:stride, 0:w:stride]
            self._grid_cache[cache_key] = (uu.astype(np.float64), vv.astype(np.float64))
        uu, vv = self._grid_cache[cache_key]
        z = depth[0:h:stride, 0:w:stride]
        finite = np.isfinite(z) & (z > 0.15) & (z < 6.0)

        x_cam = (uu - CAM_CX) * z / CAM_FX
        y_cam = (vv - CAM_CY) * z / CAM_FY
        points_cam = np.stack([x_cam, y_cam, z], axis=-1)
        points_w = points_cam @ CAM_R_WC.T + CAM_POS_W

        xw = points_w[..., 0]
        yw = points_w[..., 1]
        zw = points_w[..., 2]
        tabletop = (
            finite
            & (xw > TABLE_CENTER_X - 0.25)
            & (xw < TABLE_CENTER_X + 0.25)
            & (yw > -0.02)
            & (yw < 0.33)
            & (zw > TABLE_TOP_Z + 0.006)
            & (zw < TABLE_TOP_Z + 0.26)
        )

        bands = {
            3: (TABLE_CENTER_Y + 0.00, TABLE_CENTER_Y + 0.11),
            2: (TABLE_CENTER_Y + 0.10, TABLE_CENTER_Y + 0.22),
            1: (TABLE_CENTER_Y + 0.21, TABLE_CENTER_Y + 0.33),
        }
        targets: list[TargetObject] = []
        for object_id in (3, 2, 1):
            lo, hi = bands[object_id]
            mask = tabletop & (yw >= lo) & (yw <= hi)
            if int(mask.sum()) < 12:
                targets.append(TargetObject(object_id, self._fallback_pos(object_id)))
                continue
            xs = xw[mask]
            ys = yw[mask]
            zs = zw[mask]
            pos = np.array(
                [
                    float(np.clip(np.median(xs), TABLE_CENTER_X - 0.11, TABLE_CENTER_X + 0.11)),
                    float(np.clip(np.median(ys), lo + 0.01, hi - 0.01)),
                    float(np.percentile(zs, 65)),
                ],
                dtype=np.float64,
            )
            pos = pos + TARGET_CENTER_OFFSETS.get(object_id, 0.0)
            pos[0] = float(np.clip(pos[0], TABLE_CENTER_X - 0.11, TABLE_CENTER_X + 0.11))
            pos[1] = float(np.clip(pos[1], lo + 0.01, hi - 0.01))
            targets.append(TargetObject(object_id, pos))
        return targets

    def _fallback_targets(self) -> list[TargetObject]:
        return [TargetObject(i, self._fallback_pos(i)) for i in (3, 2, 1)]

    def _detect_basket(self, obs) -> np.ndarray:
        image = obs.get("image", {})
        if "video_depth" not in image or image["video_depth"] is None:
            return BASKET_CENTER_W.copy()

        depth = _as_numpy(image["video_depth"])
        if depth.ndim == 4:
            depth = depth[0, :, :, 0]
        elif depth.ndim == 3:
            depth = depth[0] if depth.shape[0] == 1 else depth[:, :, 0]
        depth = depth.astype(np.float64)

        h, w = depth.shape
        stride = 4
        cache_key = (h, w, stride)
        if cache_key not in self._grid_cache:
            vv, uu = np.mgrid[0:h:stride, 0:w:stride]
            self._grid_cache[cache_key] = (uu.astype(np.float64), vv.astype(np.float64))
        uu, vv = self._grid_cache[cache_key]
        z = depth[0:h:stride, 0:w:stride]
        finite = np.isfinite(z) & (z > 0.15) & (z < 6.0)

        x_cam = (uu - CAM_CX) * z / CAM_FX
        y_cam = (vv - CAM_CY) * z / CAM_FY
        points_cam = np.stack([x_cam, y_cam, z], axis=-1)
        points_w = points_cam @ CAM_R_WC.T + CAM_POS_W

        xw = points_w[..., 0]
        yw = points_w[..., 1]
        zw = points_w[..., 2]
        basket = (
            finite
            & (xw > BASKET_CENTER_W[0] - 0.24)
            & (xw < BASKET_CENTER_W[0] + 0.24)
            & (yw > BASKET_CENTER_W[1] - 0.18)
            & (yw < BASKET_CENTER_W[1] + 0.18)
            & (zw > TABLE_TOP_Z + 0.02)
            & (zw < TABLE_TOP_Z + 0.35)
        )
        if int(basket.sum()) < 20:
            return BASKET_CENTER_W.copy()

        return np.array(
            [
                float(np.clip(np.median(xw[basket]), BASKET_CENTER_W[0] - 0.08, BASKET_CENTER_W[0] + 0.08)),
                float(np.clip(np.median(yw[basket]), BASKET_CENTER_W[1] - 0.08, BASKET_CENTER_W[1] + 0.08)),
                TABLE_TOP_Z + 0.15,
            ],
            dtype=np.float64,
        )

    def _fallback_pos(self, object_id: int) -> np.ndarray:
        y = {1: 0.25, 2: 0.16, 3: 0.06}.get(object_id, 0.06)
        return np.array([TABLE_CENTER_X, TABLE_CENTER_Y + y, TABLE_TOP_Z + 0.04], dtype=np.float64)
