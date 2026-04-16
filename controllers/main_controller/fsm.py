from config import *
import random

class FSM:
    def __init__(self):
        self.state = "EXPLORE"

        # Counters for stability
        self.stuck_counter = 0
        self.avoid_counter = 0
        self.wall_counter = 0
        self.state_confirm_counter = 0

        # Last action for stuck detection / corridor stability
        self.last_action = "MOVE_FORWARD"

        # Escape turn memory for AVOID
        self.escape_turn = "RIGHT"

        # Light memory to prevent repeated turns
        self.turn_memory = []

        # Last front sensor
        self.last_front = None

    # -------------------------
    # STATE UPDATE
    # -------------------------
    def update(self, sensor, goal_detected):
        front = sensor["front"]
        left = sensor["left"]
        right = sensor["right"]

        diff = left - right

        # -------------------------
        # GOAL CHECK (external now)
        # -------------------------
        if goal_detected:
            self.state = "GOAL_REACHED"
            self.last_action = "STOP"
            return

        # -------------------------
        # STUCK DETECTION → RECOVERY
        # -------------------------
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

        # -------------------------
        # AVOID STATE ENTRY
        # -------------------------
        if front > FRONT_AVOID_ON and self.state != "AVOID":
            self.state = "AVOID"
            self.avoid_counter = 0
            return

        # -------------------------
        # WALL FOLLOW DETECTION
        # -------------------------
        if abs(diff) > WALL_DEADZONE:
            self.wall_counter += 1
        else:
            self.wall_counter = 0

        if self.wall_counter > STATE_CONFIRM_COUNT:
            self.state = "WALL_FOLLOW"
        elif self.wall_counter == 0:
            if self.state not in ["AVOID", "RECOVERY"]:
                self.state = "EXPLORE"

    # -------------------------
    # ACTION OUTPUT
    # -------------------------
    def get_action(self, sensor):
        front = sensor["front"]
        left = sensor["left"]
        right = sensor["right"]

        diff = left - right

        # -------------------------
        # GOAL → STOP
        # -------------------------
        if self.state == "GOAL_REACHED":
            return "STOP"

        # -------------------------
        # RECOVERY
        # -------------------------
        if self.state == "RECOVERY":
            return "TURN_LEFT" if left < right else "TURN_RIGHT"

        # -------------------------
        # AVOID
        # -------------------------
        if self.state == "AVOID":
            self.avoid_counter += 1

            if self.avoid_counter == 1:
                self.escape_turn = "LEFT" if left < right else "RIGHT"

            if self.avoid_counter < ESCAPE_LIMIT:
                return "TURN_LEFT" if self.escape_turn == "LEFT" else "TURN_RIGHT"
            else:
                self.state = "EXPLORE"
                self.avoid_counter = 0
                return "MOVE_FORWARD"

        # -------------------------
        # WALL FOLLOW
        # -------------------------
        if self.state == "WALL_FOLLOW":
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

        # -------------------------
        # EXPLORE
        # -------------------------
        action = "MOVE_FORWARD"

        if self.last_action == "MOVE_FORWARD":
            self.state_confirm_counter += 1
        else:
            self.state_confirm_counter = 0

        if self.state_confirm_counter > (STUCK_LIMIT // 2):
            self.state_confirm_counter = 0
            action = "SLIGHT_RIGHT" if left > right else "SLIGHT_LEFT"

        if front > 30 and abs(left - right) > 5:
            action = "SLIGHT_RIGHT" if left > right else "SLIGHT_LEFT"

        self.turn_memory.append(action)
        if len(self.turn_memory) > 6:
            self.turn_memory.pop(0)

        if self.turn_memory.count(action) > 3:
            action = "MOVE_FORWARD"

        if self.state == "EXPLORE":
            if random.random() < 0.05:
                action = random.choice(["TURN_LEFT", "TURN_RIGHT"])

        self.last_action = action
        return action