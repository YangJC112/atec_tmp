# Task E ACT Demo Usage

The official evaluator imports `demo/solution.py`. To run the ACT baseline,
copy `solution_act.py` to `solution.py` before launching the official play or
submission entrypoint.

It expects:

- `demo/policy_act.pt`
- `demo/act/detr/*.py`
- observations with `proprio` and `image.video_rgb`

The policy file is not committed because model weights are large. The guide says to
copy the provided baseline checkpoint:

```bash
cp ../atec_robot_model/baseline/act/policy.pt demo/policy_act.pt
cp demo/solution_act.py demo/solution.py
python scripts/play_atec_task.py --task ATEC-TaskE-Piper --headless --enable_cameras
```

`solution_act.py` first drives Piper to a teleop home pose, then converts the
relative joint-position observation to absolute joint positions, resizes
`video_rgb` to 224x224, and calls ACT to output the 8-D action.
