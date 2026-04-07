from config import FORWARD_SPEED, TURN_SPEED, SLIGHT_SPEED_DIFF

MAX_SPEED = 6.28  # e-puck limit

def clamp(speed):
    return max(-MAX_SPEED, min(MAX_SPEED, speed))


def move_forward(left_motor, right_motor):
    left_motor.setVelocity(clamp(FORWARD_SPEED))
    right_motor.setVelocity(clamp(FORWARD_SPEED))


def turn_left(left_motor, right_motor):
    left_motor.setVelocity(clamp(-TURN_SPEED))
    right_motor.setVelocity(clamp(TURN_SPEED))


def turn_right(left_motor, right_motor):
    left_motor.setVelocity(clamp(TURN_SPEED))
    right_motor.setVelocity(clamp(-TURN_SPEED))


def slight_left(left_motor, right_motor):
    left = FORWARD_SPEED - SLIGHT_SPEED_DIFF
    right = FORWARD_SPEED + SLIGHT_SPEED_DIFF
    left_motor.setVelocity(clamp(left))
    right_motor.setVelocity(clamp(right))


def slight_right(left_motor, right_motor):
    left = FORWARD_SPEED + SLIGHT_SPEED_DIFF
    right = FORWARD_SPEED - SLIGHT_SPEED_DIFF
    left_motor.setVelocity(clamp(left))
    right_motor.setVelocity(clamp(right))


def stop(left_motor, right_motor):
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)