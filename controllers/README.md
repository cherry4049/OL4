# Controllers Folder

This folder contains all the **robot controller source code** for the Maze Robot project in Webots.  
Each file has a specific purpose related to the robot’s behaviour, sensors, and movement.

---

## File Overview

### 1. `main_controller.py`

- **Purpose:** Main control loop of the robot.
- Implements the **FSM (Finite State Machine)** or behaviour tree.
- Integrates **sensor readings** and **movement commands**.
- Handles **state transitions** based on multi-condition logic.

### 2. `sensors.py`

- **Purpose:** Handles all sensor data collection and processing.
- Reads data from **distance sensors**, wall detectors, or other perception sources.
- Processes sensor data and sends it to `main_controller.py` for decision making.

### 3. `movement.py`

- **Purpose:** Controls the robot’s actuators.
- Sends commands to wheels or motors to **move forward, turn, or stop**.
- Receives movement instructions from `main_controller.py`.

### 4. `utils.py` (optional)

- **Purpose:** Helper functions used across multiple files.
- Can include **math functions**, **decision helpers**, or any reusable code.
- Not strictly required but helps keep code modular and clean.

---

## Notes

- Each file is designed to minimize conflicts between team members.
- Branches in Git correspond to files:
  - `feature/fsm` → `main_controller.py`
  - `feature/sensors` → `sensors.py`
  - `feature/movement` → `movement.py`
  - `feature/world` → `worlds/world.wbt`
- Placeholders are included for each file to allow GitHub to display the folder structure.

---

## Workflow Tip

- Each team member works mainly in their assigned file/branch.
- Merge completed branches into `develop` for integration before final submission.
