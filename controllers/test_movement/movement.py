# movement.py
# Purpose: Motor control functions for e-puck movements

MAX_SPEED = 6.28  # Default max wheel speed (rad/s)

def move_forward(left_motor, right_motor, speed=MAX_SPEED):
    """Move both wheels forward at the given speed."""
    left_motor.setVelocity(speed)
    right_motor.setVelocity(speed)

def turn_left(left_motor, right_motor, speed=MAX_SPEED):
    """Rotate robot left in place: left wheel backward, right wheel forward."""
    left_motor.setVelocity(-speed)
    right_motor.setVelocity(speed)

def turn_right(left_motor, right_motor, speed=MAX_SPEED):
    """Rotate robot right in place: left wheel forward, right wheel backward."""
    left_motor.setVelocity(speed)
    right_motor.setVelocity(-speed)

def stop(left_motor, right_motor):
    """Stop both wheels immediately (idle or emergency stop)."""
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)