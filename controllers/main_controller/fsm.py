from config import (
    STUCK_LIMIT,
    FRONT_AVOID_ON,
    FRONT_AVOID_OFF,
    WALL_DIFF_SMALL,
    WALL_DIFF_STRONG,
    STATE_CONFIRM_COUNT
)


class FSM:
    def __init__(self):
        self.state = "EXPLORE"

        # Memory
        self.last_action = "MOVE_FORWARD"
        self.last_turn = None

        # Counters
        self.avoid_counter = 0
        self.stuck_counter = 0
        self.wall_counter = 0
        self.straight_counter = 0

        # Memory-lite (VERY IMPORTANT for loop prevention)
        self.turn_memory = []

        self.last_front = None
        self.escape_turn = "RIGHT"

    # -----------------------
    # STATE UPDATE
    # -----------------------
    def update(self, sensor_data):
        front = sensor_data["front"]
        left = sensor_data["left"]
        right = sensor_data["right"]

        # -----------------------
        # STUCK DETECTION
        # -----------------------
        if self.last_front is not None:
            if abs(front - self.last_front) < 0.5:
                self.stuck_counter += 1
            else:
                self.stuck_counter = 0

        self.last_front = front

        if self.stuck_counter > STUCK_LIMIT:
            self.state = "RECOVERY"
            self.stuck_counter = 0
            return

        # -----------------------
        # GOAL / EXIT DETECTION (CRITICAL FIX)
        # -----------------------
        if front < 8 and left < 8 and right < 8:
            self.state = "GOAL_REACHED"
            return

        # -----------------------
        # OBSTACLE AVOID ENTRY
        # -----------------------
        if self.state != "AVOID" and front > FRONT_AVOID_ON:
            self.state = "AVOID"
            self.avoid_counter = 0
            return

        # -----------------------
        # OBSTACLE AVOID EXIT
        # -----------------------
        if self.state == "AVOID":
            if front < FRONT_AVOID_OFF:
                self.state = "EXPLORE"
                self.avoid_counter = 0
            return

        # -----------------------
        # WALL FOLLOW DETECTION
        # -----------------------
        if abs(left - right) > WALL_DIFF_SMALL:
            self.wall_counter += 1
        else:
            self.wall_counter = 0

        if self.wall_counter > STATE_CONFIRM_COUNT:
            self.state = "WALL_FOLLOW"
        else:
            self.state = "EXPLORE"

    # -----------------------
    # ACTION DECISION
    # -----------------------
    def get_action(self, sensor_data):
        front = sensor_data["front"]
        left = sensor_data["left"]
        right = sensor_data["right"]

        # -----------------------
        # PRIORITY 1: GOAL (ABSOLUTE STOP)
        # -----------------------
        if self.state == "GOAL_REACHED":
            return "STOP"

        # -----------------------
        # RECOVERY
        # -----------------------
        if self.state == "RECOVERY":
            return "TURN_LEFT" if left < right else "TURN_RIGHT"

        # -----------------------
        # AVOID
        # -----------------------
        if self.state == "AVOID":
            self.avoid_counter += 1

            if self.avoid_counter == 1:
                self.escape_turn = "LEFT" if left < right else "RIGHT"

            if self.avoid_counter < 6:
                return "TURN_LEFT" if self.escape_turn == "LEFT" else "TURN_RIGHT"

            elif self.avoid_counter < 12:
                return "MOVE_FORWARD"

            else:
                self.state = "EXPLORE"
                self.avoid_counter = 0
                return "MOVE_FORWARD"

        # -----------------------
        # WALL FOLLOW (RIGHT-HAND RULE HYBRID)
        # -----------------------
        if self.state == "WALL_FOLLOW":
            diff = left - right

            if diff > WALL_DIFF_STRONG:
                return "TURN_RIGHT"
            elif diff < -WALL_DIFF_STRONG:
                return "TURN_LEFT"
            elif diff > WALL_DIFF_SMALL:
                return "SLIGHT_RIGHT"
            elif diff < -WALL_DIFF_SMALL:
                return "SLIGHT_LEFT"
            else:
                return "MOVE_FORWARD"

        # -----------------------
        # EXPLORE (SAFE MODE - NO ESCAPE BUG)
        # -----------------------
        if self.state == "EXPLORE":

            # SAFE OPEN SPACE DEFINITION (CRITICAL FIX)
            open_space = front > 20 and left > 20 and right > 20

            # -----------------------
            # CORRIDOR STABILITY
            # -----------------------
            if self.last_action == "MOVE_FORWARD":
                self.straight_counter += 1
            else:
                self.straight_counter = 0

            if self.straight_counter > 25:
                self.straight_counter = 0
                return "SLIGHT_LEFT" if left > right else "SLIGHT_RIGHT"

            # -----------------------
            # OPEN SPACE CONTROL (NO ESCAPE)
            # -----------------------
            if open_space:
                return "SLIGHT_LEFT" if left > right else "SLIGHT_RIGHT"

            # -----------------------
            # WALL GUIDANCE
            # -----------------------
            if left > right + 3:
                action = "SLIGHT_RIGHT"
            elif right > left + 3:
                action = "SLIGHT_LEFT"
            else:
                action = "MOVE_FORWARD"

            # -----------------------
            # LOOP PREVENTION (LIGHT MEMORY)
            # -----------------------
            self.turn_memory.append(action)
            if len(self.turn_memory) > 6:
                self.turn_memory.pop(0)

            if self.turn_memory.count(action) > 3:
                action = "MOVE_FORWARD"

            self.last_action = action
            return action

        # -----------------------
        # SAFETY FALLBACK
        # -----------------------
        return "STOP"