from config import FORWARD_SPEED, TURN_SPEED

def move_forward(left_motor, right_motor):
    left_motor.setVelocity(FORWARD_SPEED)
    right_motor.setVelocity(FORWARD_SPEED)
 
def turn_left(left_motor, right_motor):
    left_motor.setVelocity(-TURN_SPEED)
    right_motor.setVelocity(TURN_SPEED)
    
def turn_right(left_motor, right_motor):
    left_motor.setVelocity(TURN_SPEED)
    right_motor.setVelocity(-TURN_SPEED)

def stop(left_motor, right_motor):
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)