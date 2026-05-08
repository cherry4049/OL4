from config import *

class FSM:
    def __init__(self):
        self.state = "EXPLORE"
        self._stuck_counter = 0
        self._recovery_counter = 0
        self._prev_enc_left = None   # encoder tracking

    def update(self, sensor, goal_detected):

        # -------------------------
        # GOAL STATE
        # -------------------------
        if goal_detected:
            self.state = "GOAL_REACHED"
            self._stuck_counter = 0
            return

        # -------------------------
        # RECOVERY STATE
        # -------------------------
        if self.state == "RECOVERY":
            self._recovery_counter += 1

            if self._recovery_counter >= RECOVERY_STEPS:
                self.state = "EXPLORE"
                self._recovery_counter = 0
                self._stuck_counter = 0

            self._prev_enc_left = sensor.get("enc_left", 0)
            return

        front = sensor["front"]
        right = sensor["right"]

        # -------------------------
        # ENCODER STUCK CHECK
        # -------------------------
        curr_enc_left = sensor.get("enc_left", 0)

        if self._prev_enc_left is None:
            self._prev_enc_left = curr_enc_left

        encoder_not_moving = abs(curr_enc_left - self._prev_enc_left) < 0.001
        self._prev_enc_left = curr_enc_left

        # -------------------------
        # OBSTACLE / STUCK
        # -------------------------
        if front > FRONT_AVOID_ON or encoder_not_moving:
            self._stuck_counter += 1

            if self._stuck_counter >= STUCK_TIME_LIMIT:
                self.state = "RECOVERY"
                self._recovery_counter = 0
            else:
                self.state = "AVOID"

            return

        self._stuck_counter = 0

        # -------------------------
        # WALL DETECTION
        # -------------------------
        if right > WALL_THRESHOLD:
            self.state = "WALL_FOLLOW"
        else:
            self.state = "EXPLORE"

    def get_action(self, sensor):

        front = sensor["front"]
        right = sensor["right"]

        # -------------------------
        # GOAL
        # -------------------------
        if self.state == "GOAL_REACHED":
            return ("STOP", 0)

        # -------------------------
        # RECOVERY
        # -------------------------
        if self.state == "RECOVERY":
            return ("TURN_LEFT", 0)

        # -------------------------
        # AVOID
        # -------------------------
        if self.state == "AVOID":
            return ("TURN_LEFT", 0)

        # -------------------------
        # WALL FOLLOW (FIXED CONTROL)
        # -------------------------
        if self.state == "WALL_FOLLOW":

            # emergency correction if too close
            if front > FRONT_AVOID_ON:
                return ("TURN_LEFT", 0)

            # stable right-wall tracking (NO dead-zone)
            error = right - DESIRED_RIGHT

            # proportional-like correction (more stable than thresholds)
            if error > WALL_DIFF:
                return ("SLIGHT_LEFT", 0)

            elif error < -WALL_DIFF:
                return ("SLIGHT_RIGHT", 0)

            return ("MOVE_FORWARD", 0)

        # -------------------------
        # EXPLORE
        # -------------------------
        if self.state == "EXPLORE":

            if right < WALL_THRESHOLD:
                return ("TURN_RIGHT", 0)

            if front > FRONT_AVOID_ON:
                return ("TURN_LEFT", 0)

            return ("MOVE_FORWARD", 0)