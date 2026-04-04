from config import FRONT_THRESHOLD, LEFT_THRESHOLD, RIGHT_THRESHOLD


class FSM:
    def __init__(self):
        self.state = "EXPLORE"
        self.avoid_counter = 0

    def update(self, sensor_data):
        front = sensor_data["front"]
        left = sensor_data["left"]
        right = sensor_data["right"]

        # -----------------------
        # PRIORITY 1: OBSTACLE AHEAD
        # -----------------------
        if front < FRONT_THRESHOLD:
            self.state = "AVOID"
            self.avoid_counter = 0
            return

        # -----------------------
        # PRIORITY 2: WALL DETECTION
        # -----------------------
        # If either side detects a wall (using threshold)
        if left > LEFT_THRESHOLD or right > RIGHT_THRESHOLD:
            self.state = "WALL_FOLLOW"
        else:
            self.state = "EXPLORE"

        # -----------------------
        # AVOID TIMER (prevents infinite avoid state)
        # -----------------------
        if self.state == "AVOID":
            self.avoid_counter += 1
            if self.avoid_counter > 20:
                self.state = "EXPLORE"
                self.avoid_counter = 0

    def get_action(self, sensor_data):
        front = sensor_data["front"]
        left = sensor_data["left"]
        right = sensor_data["right"]

        # Debug (keep while testing)
        print("STATE:", self.state, "| F:", front, "L:", left, "R:", right)

        # -----------------------
        # EXPLORE MODE
        # -----------------------
        if self.state == "EXPLORE":
            return "MOVE_FORWARD"

        # -----------------------
        # WALL FOLLOW MODE
        # -----------------------
        elif self.state == "WALL_FOLLOW":
            # small difference filter to avoid noise
            diff = left - right

            if diff > 5:
                print("TURN RIGHT")
                return "TURN_RIGHT"
            elif diff < -5:
                print("TURN LEFT")
                return "TURN_LEFT"
            else:
                return "MOVE_FORWARD"

        # -----------------------
        # AVOID MODE
        # -----------------------
        elif self.state == "AVOID":
            # simple escape behaviour
            if left < right:
                print("AVOID → TURN LEFT")
                return "TURN_LEFT"
            else:
                print("AVOID → TURN RIGHT")
                return "TURN_RIGHT"

        # -----------------------
        # SAFETY FALLBACK
        # -----------------------
        return "STOP"