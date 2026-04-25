MAX_SPEED = 6.0

def clamp(v):
    return max(-MAX_SPEED, min(MAX_SPEED, v))


def wall_follow(left_motor, right_motor, left, right, front):
    base = 3.0
    error = left - right

    left_speed = base + error * 0.003
    right_speed = base - error * 0.003

    left_motor.setVelocity(clamp(left_speed))
    right_motor.setVelocity(clamp(right_speed))


def turn_left(left_motor, right_motor):
    left_motor.setVelocity(-3)
    right_motor.setVelocity(3)


def turn_right(left_motor, right_motor):
    left_motor.setVelocity(3)
    right_motor.setVelocity(-3)


def escape(left_motor, right_motor):
    left_motor.setVelocity(-2)
    right_motor.setVelocity(-2)


def stop(left_motor, right_motor):
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)