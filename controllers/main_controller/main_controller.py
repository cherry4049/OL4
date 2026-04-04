from controller import Robot
from sensors import Sensors
from fsm import FSM
import movement

def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())
    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")

    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    # Initialise proximity sensors
    #--------------
    ps = []
    for i in range(8):
        ps.append(robot.getDevice(f"ps{i}"))
        ps[i].enable(timestep)
    #-------------------------

    # Initialise modules
    sensors = Sensors(robot, ps)
    fsm = FSM()

    while robot.step(timestep) != -1:
        # 1. Read sensor data
        sensor_data = sensors.read()

        print(sensor_data) # log for debugging

        # 2. Update FSM
        fsm.update(sensor_data)

        # 3. Get action from FSM
        action = fsm.get_action()

        # 4. Execute action
        if action == "MOVE_FORWARD":
            movement.move_forward(left_motor, right_motor)
        elif action == "TURN_LEFT":
            movement.turn_left(left_motor, right_motor)
        elif action == "TURN_RIGHT":
            movement.turn_right(left_motor, right_motor)
        else:
            movement.stop(left_motor, right_motor)


if __name__ == "__main__":
    main()