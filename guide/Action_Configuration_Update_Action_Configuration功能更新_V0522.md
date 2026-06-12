# Action Configuration Update

### 1. 公告

【更新公告】
本次更新增加了選手自訂 Action Configuration 的功能。選手現在可透過 `solution.py` 中的 `get_action_spec()` 函數來設定機器人關節的控制類型（如角度、速度或力矩）、scale 與 clip 參數。同時，在 `server.py` 中新增了 `/get_action_spec` 介面，供打分程式調用以取得此自訂配置。詳細使用方法請參考選手指南與 README 文件。

### 2. 選手指南（機器人控制後）

#### 自訂 Action 配置

選手可以選擇在 `solution.py` 中實作 `AlgSolution.get_action_spec()`，從而自訂 action 配置。

如果 `get_action_spec()` 傳回 `None`，則使用官方預設的 action 配置。

`solution.py` 中新增 `get_action_spec()` 方法：
```py
from typing import Any


class AlgSolution:
 def get_action_spec(self) -> dict[str, dict[str, Any]] | None:
 return None

 def predicts(self, obs, current_score):
 ...
```

`server.py` 中新增 `/get_action_spec` 介面：
```py
@app.get('/get_action_spec')
async def get_action_spec():
    if hasattr(agent, 'get_action_spec'):
        return agent.get_action_spec()
    logger.warning("'get_action_spec' not found in solution")
    return {}
```

傳回的 action spec 是一個字典，其 key 為 action group：

- `leg`：腿部關節
- `wheel`：輪子關節
- `arm`：機械臂關節

每個 group 可以定義以下欄位：

- `mode`：可選 `"position"`、`"velocity"` 或 `"effort"`
- `scale`：正浮點數
- `clip`：`None` 或 `[min, max]`

示例：

```python
from typing import Any


class AlgSolution:
 def get_action_spec(self) -> dict[str, dict[str, Any]] | None:
 return {
 "leg": {
 "mode": "position",
 "scale": 1.0,
 "clip": [-10.0, 10.0],
 },
 "wheel": {
 "mode": "velocity",
 "scale": 2.0,
 "clip": [-11.0, 11.0],
 },
 "arm": {
 "mode": "effort",
 "scale": 3.0,
 "clip": [-12.0, 12.0],
 },
 }

 def predicts(self, obs, current_score):
 ...
```

注意事項：

- 未填寫的 action group 會使用官方預設配置。
- 如果某個機器人不包含指定的 action group，則該 group 會被忽略。
- 關節名稱和關節順序會自動繼承所選 task 和 robot 的官方配置，選手不需要也不能手動指定。

---

### 1. 公告

【更新公告】
本次更新增加了选手自定义 Action Configuration 的功能。选手现在可通过 `solution.py` 中的 `get_action_spec()` 函数来配置机器人关节的控制类型（如角度、速度或力矩）、scale 与 clip 参数。同时，在 `server.py` 中新增了 `/get_action_spec` 接口，供打分程序调用以获取此自定义配置。详细使用方法请参考选手指南与 README 文件。

### 2. 选手指南（机器人控制后）

#### 自定义 Action 配置

选手可以选择在 `solution.py` 中实现 `AlgSolution.get_action_spec()`，从而自定义 action 配置。

如果 `get_action_spec()` 返回 `None`，则使用官方默认的 action 配置。

`solution.py` 中新增 `get_action_spec()` 方法：
```py
from typing import Any


class AlgSolution:
 def get_action_spec(self) -> dict[str, dict[str, Any]] | None:
 return None

 def predicts(self, obs, current_score):
 ...
```

`server.py` 中新增 `/get_action_spec` 接口：
```py
@app.get('/get_action_spec')
async def get_action_spec():
    if hasattr(agent, 'get_action_spec'):
        return agent.get_action_spec()
    logger.warning("'get_action_spec' not found in solution")
    return {}
```

返回的 action spec 是一个字典，其 key 为 action group：

- `leg`：腿部关节
- `wheel`：轮子关节
- `arm`：机械臂关节

每个 group 可以定义以下字段：

- `mode`：可选 `"position"`、`"velocity"` 或 `"effort"`
- `scale`：正浮点数
- `clip`：`None` 或 `[min, max]`

示例：

```python
from typing import Any


class AlgSolution:
 def get_action_spec(self) -> dict[str, dict[str, Any]] | None:
 return {
 "leg": {
 "mode": "position",
 "scale": 1.0,
 "clip": [-10.0, 10.0],
 },
 "wheel": {
 "mode": "velocity",
 "scale": 2.0,
 "clip": [-11.0, 11.0],
 },
 "arm": {
 "mode": "effort",
 "scale": 3.0,
 "clip": [-12.0, 12.0],
 },
 }

 def predicts(self, obs, current_score):
 ...
```

注意事项：

- 未填写的 action group 会使用官方默认配置。
- 如果某个机器人不包含指定的 action group，则该 group 会被忽略。
- 关节名称和关节顺序会自动继承所选 task 和 robot 的官方配置，选手不需要也不能手动指定。

---

### 1. Notice

【Update Notice】
This update introduces the ability for participants to customize the Action Configuration. Participants can now configure the robot joint control types (e.g., position, velocity, or torque), scale, and clip parameters via the `get_action_spec()` function in `solution.py`. Additionally, a new `/get_action_spec` endpoint has been added in `server.py` for the scoring program to retrieve this custom configuration. For detailed usage, please refer to the Participant Guide and README documentation.

### 2. Participant Guide (After Robot Control)

#### Custom Action Configuration

Participants may optionally customize the action configuration in `demo/solution.py` by implementing `AlgSolution.get_action_spec()`.

If `get_action_spec()` returns `None`, the official default action configuration is used.

Added the `get_action_spec()` method in `solution.py`:
```py
from typing import Any


class AlgSolution:
 def get_action_spec(self) -> dict[str, dict[str, Any]] | None:
 return None

 def predicts(self, obs, current_score):
 ...
```

Added the `/get_action_spec` endpoint in `server.py`:
```py
@app.get('/get_action_spec')
async def get_action_spec():
    if hasattr(agent, 'get_action_spec'):
        return agent.get_action_spec()
    logger.warning("'get_action_spec' not found in solution")
    return {}
```

The returned action spec is a dictionary whose keys are action groups:

- `leg`: leg joints
- `wheel`: wheel joints
- `arm`: manipulator joints

Each group may define the following fields:

- `mode`: one of `"position"`, `"velocity"`, or `"effort"`
- `scale`: positive float
- `clip`: `None` or `[min, max]`

Example:

```python
from typing import Any


class AlgSolution:
 def get_action_spec(self) -> dict[str, dict[str, Any]] | None:
 return {
 "leg": {
 "mode": "position",
 "scale": 1.0,
 "clip": [-10.0, 10.0],
 },
 "wheel": {
 "mode": "velocity",
 "scale": 2.0,
 "clip": [-11.0, 11.0],
 },
 "arm": {
 "mode": "effort",
 "scale": 3.0,
 "clip": [-12.0, 12.0],
 },
 }

 def predicts(self, obs, current_score):
 ...
```

Notes:

- Missing groups use the official default configuration.
- If a robot does not have a requested action group, that group is ignored.
- The joint names and joint order are inherited from the selected task and robot.
