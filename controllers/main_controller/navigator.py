from movement import set_speed

def navigate(left_motor, right_motor, state, sensor):

    # HARD STATES
    if state == "GOAL_REACHED":
        set_speed(left_motor, right_motor, 0, 0)
        return

    if state == "ESCAPE":
        set_speed(left_motor, right_motor, 2.5, -2.5)
        return

    if state == "TURN_RIGHT":
        set_speed(left_motor, right_motor, 2.2, -2.2)
        return

    # LEFT WALL FOLLOWING - SIMPLE FIX
    BASE = 3.0
    TARGET = 80  # Adjust this value to change distance from wall

    # Distance control
    dist_error = sensor["left"] - TARGET
    if abs(dist_error) < 5:
        dist_error = 0
    dist_correction = 0.008 * dist_error

    # ANGLE CONTROL - THE FIX (head sticky means turn RIGHT)
    front_left = sensor["raw"][7]   # PS7 - front-left
    back_left = sensor["raw"][4]    # PS4 - back-left
    
    # If front_left > back_left: head is closer -> need to turn RIGHT
    # Turning RIGHT means left wheel faster than right wheel
    angle_error = front_left - back_left
    
    # Strong angle correction (increase if still sticky)
    angle_correction = 0.015 * angle_error  # Positive = turn RIGHT

    # Combine: when head sticky (positive angle_correction), turn RIGHT
    # Right turn = left wheel faster
    l = BASE + angle_correction - dist_correction
    r = BASE - angle_correction + dist_correction

    # Safety limits
    l = max(0.5, min(4.0, l))
    r = max(0.5, min(4.0, r))

    # Front obstacle avoidance
    if sensor["front"] > 180:
        set_speed(left_motor, right_motor, -1.5, 2.5)
        return

    set_speed(left_motor, right_motor, l, r)