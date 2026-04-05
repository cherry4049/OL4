from controller import Robot
from sensors import Sensors
from fsm import FSM
from config import FRONT_THRESHOLD, LEFT_THRESHOLD, RIGHT_THRESHOLD, FORWARD_SPEED
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
        sensor = robot.getDevice(f"ps{i}")
        if sensor is not None:
            sensor.enable(timestep)
            ps.append(sensor)
        else:
            print(f"Warning: ps{i} not found")
    #-------------------------

    # Initialise modules
    sensors = Sensors(robot, ps)
    fsm = FSM()

    while robot.step(timestep) != -1:
        # 1. Read sensor data
        sensor_data = sensors.read()

        print(fsm.state, sensor_data) # log for debugging

        # 2. Update FSM
        fsm.update(sensor_data)

        # 3. Get action from FSM
        action = fsm.get_action(sensor_data)

        # 4. Execute action
        if action == "MOVE_FORWARD":
            movement.move_forward(left_motor, right_motor)
        elif action == "TURN_LEFT":
            movement.turn_left(left_motor, right_motor)
        elif action == "TURN_RIGHT":
            movement.turn_right(left_motor, right_motor)
        elif action == "SLIGHT_LEFT":
            movement.slight_left(left_motor, right_motor)
        elif action == "SLIGHT_RIGHT":
            movement.slight_right(left_motor, right_motor)
        else:
            movement.stop(left_motor, right_motor)


if __name__ == "__main__":
    main()