# navigator.py

from config import MAX_SPEED

SAFE_SPEED = 4.5  # keep below Webots limit (6.28 safety margin)


def clamp_speed(v):
    if v > SAFE_SPEED:
        return SAFE_SPEED
    if v < -SAFE_SPEED:
        return -SAFE_SPEED
    return v


def set_motors(left_motor, right_motor, left_speed, right_speed):
    left_motor.setVelocity(clamp_speed(left_speed))
    right_motor.setVelocity(clamp_speed(right_speed))


# ---------------------------
# PURE ACTION FUNCTIONS
# ---------------------------

def wall_follow(left_motor, right_motor, left, right, front):
    """
    Simple reactive wall following.
    NO FSM logic here.
    """

    base = SAFE_SPEED

    # steering correction (keep simple + stable)
    error = left - right
    correction = error * 0.01  # small gain to avoid oscillation

    left_speed = base - correction
    right_speed = base + correction

    set_motors(left_motor, right_motor, left_speed, right_speed)


def avoid(left_motor, right_motor):
    """
    Simple obstacle avoidance: rotate in place.
    """

    set_motors(left_motor, right_motor, -SAFE_SPEED, SAFE_SPEED)


def recovery(left_motor, right_motor):
    """
    Back off slightly then turn.
    """

    set_motors(left_motor, right_motor, -SAFE_SPEED * 0.6, -SAFE_SPEED * 0.6)


def stop(left_motor, right_motor):
    set_motors(left_motor, right_motor, 0, 0)