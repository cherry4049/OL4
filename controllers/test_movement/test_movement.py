# test_movement.py


from controller import Robot
from movement import move_forward, turn_left, turn_right, stop

# ----------------------------
# Configuration
# ----------------------------
TIME_STEP = 64   # Webots simulation step in ms

# ----------------------------
# Initialize Robot
# ----------------------------
robot = Robot()

#Get wheel motors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

# Set motors to velocity control mode
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# ----------------------------
# Detailed step-by-step movement test
# ----------------------------
def movement_test():
    print("Starting e-puck movement test...")

    # ------------------------
    # 1. MOVE FORWARD
    # ------------------------
    print("Step 1: Moving forward")
    move_forward(left_motor, right_motor, 3.0) #move forward at half of the max speed
    for _ in range(40): #run for 40 steps (around 2.5 seconds)
        robot.step(TIME_STEP) #advance simulation by one time step

    # ------------------------
    # 2. TURN LEFT
    # ------------------------
    print("Step 2: Turning left") 
    turn_left(left_motor, right_motor, 1.5) #slightly slower turn speed for better control
    for _ in range(18): #run for 18 steps
        robot.step(TIME_STEP) #advance simulation

    # ------------------------
    # 3. RETURN TO FRONT (camera)
    # ------------------------
    print("Step 3: Returning to front")
    for step in range(18): #18 steps for smoother rotation
        turn_speed = 1.5 if step < 9 else 0.8 #slow down for smooth pause
        turn_right(left_motor, right_motor, turn_speed) #apply right turn at the selected speed
        robot.step(TIME_STEP) #advance simulation
        
        #pause halfway through the turn
        if step == 9: #halfway point
            print("Pausing for 0.3 sec")
            turn_right(left_motor, right_motor, 0.3) #very slow turn
            for _ in range(5): #around 0.3 seconds pasuse (5 steps)
                robot.step(TIME_STEP) #keep simulation running
            turn_right(left_motor, right_motor, 1.5) #resume normal turn speed

    # ------------------------
    # 4. TURN RIGHT
    # ------------------------
    print("Step 4: Turning right")
    turn_right(left_motor, right_motor, 1.5) #moderatte speed turn
    for _ in range(18): #run for 18 steps
        robot.step(TIME_STEP) #advance simulation

    # ------------------------
    # 5. STOP
    # ------------------------
    print("Step 5: Stopping")
    stop(left_motor, right_motor) #stop both wheels
    for _ in range(10):  #extra steps to ensure that the e-puck fully stops
        robot.step(TIME_STEP) #advance simulation

    print("Movement Test Completed.")

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    movement_test()