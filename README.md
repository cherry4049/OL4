# Programming for Robotics Project

## Project Overview

This project implements a simulated autonomous maze-solving robot using the Webots robotics simulator.  
The robot navigates through an unknown maze environment using distance sensors, wheel encoders, camera-based goal detection, and a Finite State Machine (FSM).

The project demonstrates key robotics concepts including:
- autonomous navigation
- obstacle avoidance
- wall-following behaviour
- reactive control systems
- sensor integration
- actuator control
- state-based robot behaviour

The robot is designed to:
- follow walls autonomously
- avoid obstacles and collisions
- recover from stuck situations
- detect and stop at the goal

---

## Group Members

- Jenjira Kongpong — s5393441  
- Xinghan Tai — S5251658  
- Yuehui Chen — S5361257  

---

## Specialisation Option

Autonomous Robot (Webots)

---

# Repository Structure

```text
OL4/
│
├── controllers/
│   └── main_controller/
│       ├── __pycache__/
│       ├── config.py
│       ├── fsm.py
│       ├── main_controller.py
│       ├── movement.py
│       └── sensors.py
│
├── diagrams/
│   ├── fsm_state_diagram.md
│   ├── system_architecture.md
│   ├── navigation_flowchart.md
│   ├── sensor_layout.mmd
│   └── wall_following_control.md
│
├── worlds/
│   ├── .maze_world.wbproj
│   └── maze_world.wbt
│
├── .gitignore
└── README.md
```

---

# Folder Details

## `controllers/`

Contains robot controller source code and documentation.

### `controllers/main_controller/`

Main robot control system implementation.

| File | Purpose |
|---|---|
| `main_controller.py` | Main loop, FSM integration, sensor processing, robot control |
| `fsm.py` | Finite State Machine controlling navigation behaviour |
| `movement.py` | Motor control with smoothing and turning logic |
| `sensors.py` | Distance sensor + encoder data processing |
| `config.py` | All tuning parameters and thresholds |

---

## `worlds/`

Contains Webots simulation environment files.

| File | Purpose |
|---|---|
| `maze_world.wbt` | Main maze simulation world |
| `.maze_world.wbproj` | Webots project configuration |

Used for:
- maze navigation testing
- wall-following evaluation
- obstacle avoidance testing
- final demonstration

---

## `diagrams/`

Contains all system design and logic diagrams for the robot.

### Diagram Files

- `fsm_state_diagram.md`  
  Finite State Machine showing transitions between robot behaviours:
  EXPLORE, WALL_FOLLOW, AVOID, RECOVERY, GOAL_REACHED.

- `system_architecture.md`  
  Overall system structure:
  Sensors → FSM → Movement → Motors

- `navigation_flowchart.md`  
  Step-by-step decision-making logic of the robot during navigation.

- `sensor_layout.md`  
  Layout of robot sensors and their roles.

- `wall_following_control.md`  
  Right-wall following control logic using:
  error = right - DESIRED_RIGHT

---

## `.gitignore`

Excludes unnecessary files such as:
- `__pycache__/`
- `.pyc`
- temporary IDE files

---

# System Architecture

The system follows a modular Sense → Process → Decide → Act architecture:

```text
Distance Sensors / Encoders / Camera
                ↓
           Sensor Processing
                ↓
         Finite State Machine
                ↓
          Movement Controller
                ↓
             Wheel Motors
```

### Responsibilities

| Module | Responsibility |
|---|---|
| Sensors | Read and process sensor inputs |
| FSM | Determine navigation behaviour |
| Movement | Execute motor commands |
| Motors | Apply movement inside Webots |

---

# Navigation Strategy

The robot uses a reactive navigation approach based on:
- right-wall following
- sensor-difference error control
- obstacle avoidance
- encoder-based stuck detection
- camera-based goal detection

The final system prioritises:
- stability
- smooth movement
- simplicity
- robustness in maze environments

---

# Key Features

- Autonomous maze navigation
- FSM-based behaviour control
- Continuous wall-following correction
- Obstacle avoidance
- Encoder-based recovery behaviour
- Camera-based goal detection
- Modular robotics architecture
- Real-time sensor processing

---

# Instructions for Running

## Requirements
- Webots Simulator
- Python controller support

## Run Steps
1. Open Webots
2. Load `maze_world.wbt`
3. Set controller to:
   ```
   main_controller
   ```
4. Run simulation

---

# Instructions for Markers

1. Open `maze_world.wbt`
2. Run simulation
3. Observe:
   - navigation behaviour
   - wall-following
   - obstacle avoidance
   - recovery system
   - goal detection
4. Review:
   - source code
   - FSM logic
   - diagrams
   - system design

---

# Notes

- Fully compatible with Webots
- All tuning parameters are in `config.py`
- System prioritises stability over complex mapping
- Designed for clear modular testing

---

# References

- Arkin, R. C. (1998). Behavior-based robotics. MIT Press.
- Corke, P. (2011). Robotics, vision and control: Fundamental algorithms in MATLAB. Springer. https://doi.org/10.1007/978-3-642-20144-8
- Michel, O. (2004). Webots™: Professional mobile robot simulation. International Journal of Advanced Robotic Systems, 1(1). https://doi.org/10.5772/5618
- Siegwart, R., Nourbakhsh, I. R., & Scaramuzza, D. (2011). Introduction to autonomous mobile robots (2nd ed.). MIT Press. https://mitpress.mit.edu/9780262015356/introduction-to-autonomous-mobile-robots/

# Acknowledgements

Thanks to all team members for their contributions, especially improvements to wall-following stability and overall navigation performance.