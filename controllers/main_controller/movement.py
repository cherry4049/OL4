from config import *

# Store previous motor speeds for smoothing
_prev_left = 0.0
_prev_right = 0.0

# UTILS FUNCTIONS
def clamp(x):
    """Clamp motor speed to safe limits."""
    return max(-MAX_SPEED, min(MAX_SPEED, x))

def smooth(target, prev):
    """Exponential smoothing to reduce abrupt changes."""
    return SMOOTHING_ALPHA * target + (1 - SMOOTHING_ALPHA) * prev

def accel_limit(target, prev):
    """Limit acceleration so motor speed changes gradually."""
    diff = target - prev
    if diff > MAX_ACCEL:
        return prev + MAX_ACCEL
    elif diff < -MAX_ACCEL:
        return prev - MAX_ACCEL
    return target

# CORE DRIVE FUNCTION
def drive(left_motor, right_motor, left_target, right_target):
    """
    Main motor control function:
    - Smooths input speeds
    - Limits acceleration
    - Clamps to safe range
    - Applies to motors
    """
    global _prev_left, _prev_right

    left = smooth(left_target, _prev_left)
    right = smooth(right_target, _prev_right)

    left = accel_limit(left, _prev_left)
    right = accel_limit(right, _prev_right)

    left = clamp(left)
    right = clamp(right)

    _prev_left = left
    _prev_right = right

    left_motor.setVelocity(left)
    right_motor.setVelocity(right)

# MOVEMENTS 
def forward(left_motor, right_motor):
    drive(left_motor, right_motor, FORWARD_SPEED, FORWARD_SPEED)

def slight_left(left_motor, right_motor):
    drive(left_motor, right_motor,
          FORWARD_SPEED - SLIGHT_SPEED,
          FORWARD_SPEED)

def slight_right(left_motor, right_motor):
    drive(left_motor, right_motor,
          FORWARD_SPEED,
          FORWARD_SPEED - SLIGHT_SPEED)

# ARC TURNS 
def turn_left(left_motor, right_motor):
    drive(left_motor, right_motor, 1.58, 3.64)

def turn_right(left_motor, right_motor):
    drive(left_motor, right_motor, 3.64, 1.58)

# STOP FUNCTION
def stop(left_motor, right_motor):
    drive(left_motor, right_motor, 0.0, 0.0)