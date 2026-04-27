from movement import set_speed

def navigate(left_motor, right_motor, state, sensor):

    # -------------------------
    # HARD STATES
    # -------------------------
    if state == "GOAL_REACHED":
        set_speed(left_motor, right_motor, 0, 0)
        return

    if state == "ESCAPE":
        set_speed(left_motor, right_motor, 2.5, -2.5)
        return

    if state == "TURN_RIGHT":
        set_speed(left_motor, right_motor, 2.2, -2.2)
        return

    # -------------------------
    # EXPLORE (SLIDING WALL FOLLOW - STABLE VERSION)
    # -------------------------

    BASE = 2.5
    TARGET = 140

    # distance control (wall distance)
    dist_error = sensor["left"] - TARGET

    if abs(dist_error) < 5:
        dist_error = 0

    k_dist = 0.008
    dist_correction = k_dist * dist_error

    # -------------------------
    # ANGLE CONTROL (SAFE VERSION)
    # -------------------------
    # FIX: always use raw fields safely
    angle_error = sensor["left_raw"] - sensor["right_raw"]

    if abs(angle_error) < 5:
        angle_error = 0

    k_angle = 0.01
    angle_correction = k_angle * angle_error

    # combine
    turn = dist_correction + angle_correction

    # -------------------------
    # FRONT SAFETY (ROBUST)
    # -------------------------
    if sensor["front"] > 180:
        set_speed(left_motor, right_motor, -1.5, 2.5)
        return

    # -------------------------
    # APPLY
    # -------------------------
    l = BASE - turn
    r = BASE + turn

    set_speed(left_motor, right_motor, l, r)