# movement.py
# Branch: feature/movement

from controller import Robot

# ----------------------------
# Configuration
# ----------------------------
TIME_STEP = 64        # Simulation step time in milliseconds 
MAX_SPEED = 6.28      # Maximum wheel speed in radians per second

# ----------------------------
# Robot Initialisation
# ----------------------------
robot = Robot()  # For controlling the e-puck robot in Webots

# Get wheel motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

# Set motors to velocity control mode (continuous rotation)
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# Start stopped
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# ----------------------------
# Movement Functions
# ----------------------------
def move_forward(speed=MAX_SPEED):
    """Move both wheels forward at the given speed."""
    left_motor.setVelocity(speed)
    right_motor.setVelocity(speed)

def turn_left(speed=MAX_SPEED):
    """Rotate robot left in place: left wheel backward, right wheel forward."""
    left_motor.setVelocity(-speed)
    right_motor.setVelocity(speed)

def turn_right(speed=MAX_SPEED):
    """Rotate robot right in place: left wheel forward, right wheel backward."""
    left_motor.setVelocity(speed)
    right_motor.setVelocity(-speed)

def stop():
    """Stop both wheels immediately (idle or emergency stop)."""
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

# ----------------------------
# for testing movement.py only
# ----------------------------
if __name__ == "__main__":
    print("Starting e-puck movement test...")

    # ------------------------
    # 1. MOVE FORWARD
    # ------------------------
    print("Step 1: Moving forward")
    move_forward(3.0)  # Move at half max speed
    for _ in range(40):  # Run for 40 simulation steps ( around 2.5 sec)
        robot.step(TIME_STEP)

    # ------------------------
    # 2. TURN LEFT
    # ------------------------
    print("Step 2: Turning left")
    turn_left(2.0)  # Moderate speed turn
    for _ in range(20):  # Run for 20 steps (around 1.3 sec)
        robot.step(TIME_STEP)

    # ------------------------
    # 3. RETURN TO FRONT (camera)
    # ------------------------
    print("Step 3: Returning to front")
    turn_right(2.0)  # Start turning right
    for step in range(20):  # Smoother motion
        robot.step(TIME_STEP)

        # Pause halfway
        if step == 10:  # Halfway point
            print("Pausing for 0.3 second")
            stop()  # Temporarily stop robot

            # 0.3 second ≈ 5 steps (300ms / 64ms)
            for _ in range(5):
                robot.step(TIME_STEP)

            # Resume turning
            turn_right(2.0)

    # ------------------------
    # 4. TURN RIGHT
    # ------------------------
    print("Step 4: Turning right")
    turn_right(2.0)  # Moderate speed turn
    for _ in range(20):  # Run for 20 steps (around 1.3 sec)
        robot.step(TIME_STEP)
 
    # ------------------------
    # 5. STOP
    # ------------------------
    print("Step 5: Stopping")
    stop()  # Stop both wheels
    for _ in range(10):  # Extra steps to ensure full stop
        robot.step(TIME_STEP)

    print("Testing Completed") #test completed 