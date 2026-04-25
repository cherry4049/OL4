# navigator.py (V5 STABLE - FSM FRIENDLY)

from config import *

# -----------------------------
# Safety clamp (fix sensor spikes)
# -----------------------------
def clamp(v, min_v=0, max_v=300):
    if v < min_v:
        return min_v
    if v > max_v:
        return max_v
    return v


def normalize(front, left, right):
    # clamp extreme spikes first
    front = clamp(front)
    left = clamp(left)
    right = clamp(right)

    return front, left, right


# -----------------------------
# Core navigation (no FSM conflict)
# -----------------------------
def navigate(left_motor, right_motor, front, left, right):

    front, left, right = normalize(front, left, right)

    # ---- PARAMETERS (safe defaults) ----
    BASE_SPEED = 3.0
    TURN_GAIN = 0.015
    FRONT_THRESHOLD = 120

    # ---- compute balanced steering ----
    error = right - left
    turn = TURN_GAIN * error

    # slow down if front blocked
    if front > FRONT_THRESHOLD:
        base = 1.5
    else:
        base = BASE_SPEED

    # final motor speeds
    left_speed = base - turn
    right_speed = base + turn

    # clamp motor speed (IMPORTANT: fixes your warning)
    MAX_SPEED = 6.28

    left_speed = max(-MAX_SPEED, min(MAX_SPEED, left_speed))
    right_speed = max(-MAX_SPEED, min(MAX_SPEED, right_speed))

    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)


# -----------------------------
# Emergency escape (corner fix)
# -----------------------------
def escape_corner(left_motor, right_motor):
    # strong reverse + turn
    left_motor.setVelocity(-2.0)
    right_motor.setVelocity(2.0)


# -----------------------------
# Stop
# -----------------------------
def stop(left_motor, right_motor):
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)