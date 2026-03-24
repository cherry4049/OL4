# Programming for Robotics Project

## Project Overview

This project is a **simulated autonomous robot** that navigates a maze in Webots using sensors, actuators, and a finite state machine (FSM).  
The goal is to demonstrate autonomous navigation, obstacle avoidance, exit detection, and integration of robotics concepts learned during the course.

**Group Members:**

- Jenjira Kongpong s5393441,
- Xinghan TAi,
- Yuehui Chen, S5361257

**Specialisation Option:** Autonomous Robot (Webots)

---

## Repository Structure

This repository is organized to separate **code, simulation worlds, reports, video, and diagrams** for clarity.

---

### **Folder Details**

- **`controllers/`**
  - Contains all robot control code.
  - Expected files:
    - `main_controller.py` → Main FSM, sensor integration, and movement logic
    - `sensors.py` → Optional helper functions for sensor data
    - `movement.py` → Optional helper functions for wheel movement
    - Other modules as needed

- **`worlds/`**
  - Contains all Webots simulation worlds (.wbt) used for testing.
  - Example: `maze_world.wbt`

- **`report/`**
  - `pitch_document.docx` → Project proposal submitted in Week 6
  - `project_report.docx` → Final report submitted in Week 12

- **`video/`**
  - Screen-recorded demonstration of the robot navigating the maze
  - Example: `maze_demo.mp4`

- **`diagrams/`**
  - Visual aids for the project
  - Example files:
    - `fsm_diagram.png`
    - `system_architecture.png`

- **`README.md`**
  - This file, giving an overview of the project and instructions for team members and markers

- **`.gitignore`**
  - Used to exclude unnecessary or temporary files (e.g., `.pyc`, `__pycache__/`)

---

## Instructions for Team Members

1. **Add code** to the `controllers/` folder.
2. **Add simulation worlds** to the `worlds/` folder.
3. **Update reports** in the `report/` folder.
4. **Record and add the demonstration video** to the `video/` folder.
5. **Add FSM and system diagrams** to the `diagrams/` folder.
6. Commit changes frequently with meaningful messages (e.g., `Added sensor processing module`).

---

## Instructions for Markers

1. Open **Webots** and load the `.wbt` file(s) in the `worlds/` folder.
2. Run the **robot controllers** from `controllers/` to reproduce the demonstration.
3. Review **reports** and **diagrams** for FSM, system design, and behaviour logic.
4. Watch the **video** to see the robot navigating the maze and state transitions.

---

## Notes

- All source code should be compatible with **Webots simulator**.
- Team members are responsible for ensuring that the repository is **up-to-date** with the latest code, reports, diagrams, and videos.
- Clear organization ensures the project is **easy to review and assess**.
