

1. 機器人平臺新增/机器人平台新增/Robot platforms new added：

二足機械臂操作移動平台（Bipedal Mobile Manipulation Robot）：採用二足移動平台和6自由度機械臂，用於任務A、任務B和任務D。

二足机械臂操作移动平台（Bipedal Mobile Manipulation Robot）：采用二足移动平台和6自由度机械臂，用于任务A、任务B和任务D。

Bipedal Mobile Manipulation Robot: Utilizes a bipedal mobile platform and a 6-DOF robotic arm, designed for Task A, Task B, and Task D.


2. 競賽環境列表/竞赛环境列表/Competition Environment List/：

| Arena \ Robot | G1              | Tron1Piper              | Tron2ALegged              | Tron2AWheel              | B2Piper              | B2wPiper              | Piper              |
| ------------- | --------------- | ----------------------- | ------------------------- | ------------------------ | -------------------- | --------------------- | ------------------ |
| Task A        | `ATEC-TaskA-G1` | `ATEC-TaskA-Tron1Piper` | `ATEC-TaskA-Tron2ALegged` | `ATEC-TaskA-Tron2AWheel` | `ATEC-TaskA-B2Piper` | `ATEC-TaskA-B2wPiper` |                    |
| Task B        | `ATEC-TaskB-G1` | `ATEC-TaskB-Tron1Piper` | `ATEC-TaskB-Tron2ALegged` | `ATEC-TaskB-Tron2AWheel` | `ATEC-TaskB-B2Piper` | `ATEC-TaskB-B2wPiper` |                    |
| Task D        | `ATEC-TaskD-G1` | `ATEC-TaskD-Tron1Piper` | `ATEC-TaskD-Tron2ALegged` | `ATEC-TaskD-Tron2AWheel` | `ATEC-TaskD-B2Piper` | `ATEC-TaskD-B2wPiper` |                    |
| Task E        |                 |                         |                           |                          |                      |                       | `ATEC-TaskE-Piper` |


3. 各機器人關節順序/各机器人关节顺序/Per-robot joint order：

Tron2ALegged（雙足機械臂移動操作平台/二足机械臂移动操作平台/Bipedal Mobile Manipulator）：

```
"proximal_pitch_L_Joint",
"proximal_roll_L_Joint",
"proximal_yaw_L_Joint",
"knee_L_Joint",
"ankle_pitch_L_Joint",
"proximal_pitch_R_Joint",
"proximal_roll_R_Joint",
"proximal_yaw_R_Joint",
"knee_R_Joint",
"ankle_pitch_R_Joint"
"arm1_Joint", "arm2_Joint", "arm3_Joint",
"arm4_Joint", "arm5_Joint", "arm6_Joint",
"gripper1_Joint", "gripper2_Joint"
```

Tron2AWheel（二足機械臂移動操作平台/二足机械臂移动操作平台/Bipedal Mobile Manipulation Platform）：

```
"proximal_pitch_L_Joint",
"proximal_roll_L_Joint",
"proximal_yaw_L_Joint",
"knee_L_Joint",
"proximal_pitch_R_Joint",
"proximal_roll_R_Joint",
"proximal_yaw_R_Joint",
"knee_R_Joint",
"wheel_L_Joint",
"wheel_R_Joint",
"arm1_Joint", "arm2_Joint", "arm3_Joint",
"arm4_Joint", "arm5_Joint", "arm6_Joint",
"gripper1_Joint", "gripper2_Joint"
```
