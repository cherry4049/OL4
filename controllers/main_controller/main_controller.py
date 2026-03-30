from controller import Robot

from sensors import Sensors
from movement import Movement
from fsm import FSM

def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    # Initialize modules
    sensors = Sensors(robot)
    movement = Movement(robot)
    fsm = FSM()

    while robot.step(timestep) != -1:
        # 1. Read sensor data
        sensor_data = sensors.read()

        # 2. Update FSM
        fsm.update(sensor_data)

        # 3. Get action from FSM
        action = fsm.get_action()

        # 4. Execute action
        if action == "MOVE_FORWARD":
            movement.move_forward()
        elif action == "TURN_LEFT":
            movement.turn_left()
        elif action == "TURN_RIGHT":
            movement.turn_right()
        else:
            movement.stop()


if __name__ == "__main__":
    main()