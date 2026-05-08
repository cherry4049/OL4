from controller import Robot
from sensors import Sensors
from fsm import FSM
import movement
from config import *

def detect_goal(camera):
    image = camera.getImage()
    width = camera.getWidth()
    height = camera.getHeight()

    green_count = 0
    total = 0

    for dx in range(-5, 6):
        for dy in range(-4, 5):
            cx = width // 2 + dx
            cy = height // 2 + dy

            r = camera.imageGetRed(image, width, cx, cy)
            g = camera.imageGetGreen(image, width, cx, cy)
            b = camera.imageGetBlue(image, width, cx, cy)

            total += 1

            if g > r + 15 and g > b + 15:
                green_count += 1

    if total == 0:
        return False

    return (green_count / total) > 0.65

def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    # Camera
    camera = robot.getDevice("camera")
    camera.enable(timestep)

    # Wheel motors
    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")

    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    # Wheel encoders (position sensors) for motion tracking
    left_encoder = robot.getDevice("left wheel sensor")
    right_encoder = robot.getDevice("right wheel sensor")
    left_encoder.enable(timestep)
    right_encoder.enable(timestep)

    # Distance sensors
    ps = []
    for i in range(8):
        sensor = robot.getDevice(f"ps{i}")
        sensor.enable(timestep)
        ps.append(sensor)

    sensors = Sensors(robot, ps, encoders=(left_encoder, right_encoder))
    fsm = FSM()

    goal_counter = 0

    while robot.step(timestep) != -1:
        sensor_data = sensors.read()

        # -------------------------
        # GREEN DETECTION
        # -------------------------
        if detect_goal(camera):
            goal_counter += 1
        else:
            goal_counter = 0

        green_seen = goal_counter >= GOAL_CONFIRM_TIME

        # -------------------------
        # TOUCH DETECTION (ANY ANGLE)
        # -------------------------
        touching_wall = (
            sensor_data["front_left"] > GOAL_TOUCH_THRESHOLD or
            sensor_data["front_right"] > GOAL_TOUCH_THRESHOLD
        )

        goal_detected = green_seen and touching_wall

        # -------------------------
        # HARD STOP BEFORE ANY MOVE
        # -------------------------
        if goal_detected:
            print("GOAL REACHED")

            movement.stop(left_motor, right_motor)

            # Ensure full stop (no sliding)
            for _ in range(20):
                robot.step(timestep)

            break

        # -------------------------
        # NORMAL FSM
        # -------------------------
        fsm.update(sensor_data, goal_detected)
        action, _ = fsm.get_action(sensor_data)

        print(f"{fsm.state} -> {action}", sensor_data)

        if action == "MOVE_FORWARD":
            movement.forward(left_motor, right_motor)

        elif action == "SLIGHT_RIGHT":
            movement.slight_right(left_motor, right_motor)

        elif action == "SLIGHT_LEFT":
            movement.slight_left(left_motor, right_motor)

        elif action == "TURN_LEFT":
            movement.turn_left(left_motor, right_motor)

        elif action == "TURN_RIGHT":
            movement.turn_right(left_motor, right_motor)

        elif action == "STOP":
            movement.stop(left_motor, right_motor)

if __name__ == "__main__":
    main()