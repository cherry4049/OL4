from controller import Robot
from sensors import Sensors
from fsm import FSM
from navigator import navigate
from config import *

def detect_goal(camera):
    img = camera.getImage()
    w = camera.getWidth()
    h = camera.getHeight()

    g = 0
    t = 0

    for dx in range(-5, 6):
        for dy in range(-4, 5):
            x = w//2 + dx
            y = h//2 + dy

            r = camera.imageGetRed(img, w, x, y)
            gr = camera.imageGetGreen(img, w, x, y)
            b = camera.imageGetBlue(img, w, x, y)

            t += 1
            if gr > r + 15 and gr > b + 15:
                g += 1

    return t > 0 and (g / t) > 0.65


def smooth(prev, curr, alpha=0.75):
    if prev is None:
        return curr

    return {
        "front": alpha * prev["front"] + (1 - alpha) * curr["front"],
        "left": alpha * prev["left"] + (1 - alpha) * curr["left"],
        "right": alpha * prev["right"] + (1 - alpha) * curr["right"],

        # IMPORTANT: preserve raw data
        "front_raw": curr["front_raw"],
        "left_raw": curr["left_raw"],
        "right_raw": curr["right_raw"],
        "raw": curr["raw"]
    }


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    camera = robot.getDevice("camera")
    camera.enable(timestep)

    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")

    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    ps = []
    for i in range(8):
        s = robot.getDevice(f"ps{i}")
        s.enable(timestep)
        ps.append(s)

    sensors = Sensors(robot, ps)
    fsm = FSM()

    goal_counter = 0
    tick = 0
    STARTUP = 40

    prev_sensor = None

    while robot.step(timestep) != -1:

        if tick < STARTUP:
            left_motor.setVelocity(0)
            right_motor.setVelocity(0)
            tick += 1
            continue

        raw_sensor = sensors.read()
        sensor = smooth(prev_sensor, raw_sensor)
        prev_sensor = sensor

        # goal detection
        if detect_goal(camera):
            goal_counter += 1
        else:
            goal_counter = 0

        goal = goal_counter >= GOAL_CONFIRM_TIME

        fsm.update(sensor, goal)
        state = fsm.get_state()

        print("STATE:", state, sensor)

        navigate(left_motor, right_motor, state, sensor)

        tick += 1


if __name__ == "__main__":
    main()