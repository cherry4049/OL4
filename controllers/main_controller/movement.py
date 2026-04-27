MAX_SPEED = 6.0

def clamp(v):
    return max(-MAX_SPEED, min(MAX_SPEED, v))

def set_speed(left_motor, right_motor, l, r):
    left_motor.setVelocity(clamp(l))
    right_motor.setVelocity(clamp(r))

def turn_left(left_motor, right_motor):
    set_speed(left_motor, right_motor, -3, 3)

def turn_right(left_motor, right_motor):
    set_speed(left_motor, right_motor, 3, -3)

def escape(left_motor, right_motor):
    set_speed(left_motor, right_motor, -3, -3)

def stop(left_motor, right_motor):
    set_speed(left_motor, right_motor, 0, 0)