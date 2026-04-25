from controller import Robot
from sensors import Sensors
from fsm import FSM
from movement import *

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

    STARTUP = 20

    while robot.step(timestep) != -1:

        # -----------------------
        # STARTUP STABILISATION
        # -----------------------
        if tick < STARTUP:
            left_motor.setVelocity(0)
            right_motor.setVelocity(0)
            tick += 1
            continue

        sensor = sensors.read()

        if detect_goal(camera):
            goal_counter += 1
        else:
            goal_counter = 0

        goal = goal_counter >= GOAL_CONFIRM_TIME

        fsm.update(sensor, goal)
        state = fsm.get_state()

        print("STATE:", state, sensor)

        if state == "EXPLORE":
            wall_follow(left_motor, right_motor,
                        sensor["left"], sensor["right"], sensor["front"])

        elif state == "TURN_LEFT":
            turn_left(left_motor, right_motor)

        elif state == "TURN_RIGHT":
            turn_right(left_motor, right_motor)

        elif state == "ESCAPE":
            escape(left_motor, right_motor)

        elif state == "GOAL_REACHED":
            stop(left_motor, right_motor)
            break

        tick += 1


if __name__ == "__main__":
    main()