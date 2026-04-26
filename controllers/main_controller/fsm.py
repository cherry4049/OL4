class FSM:
    def __init__(self):
        self.state = "EXPLORE"

        self.WALL = 120
        self.FRONT_BLOCK = 200

        self.commit_state = None
        self.commit_timer = 0

        self.turn_timer = 0
        self.turn_direction = None

        self.diff_buffer = []

        self.left_free_count = 0
        self.right_free_count = 0

        # -------------------------
        # NEW: environment signature memory
        # -------------------------
        self.signature_history = []
        self.sig_max = 12

        # loop prevention strength
        self.revisit_penalty = 0

    # -------------------------
    # BUILD ENV SIGNATURE
    # -------------------------
    def get_signature(self, sensor):
        # coarse representation only (robust to noise)
        f = 1 if sensor["front"] > self.WALL else 0
        l = 1 if sensor["left"] > self.WALL else 0
        r = 1 if sensor["right"] > self.WALL else 0
        return (f, l, r)

    def repeated_region(self, sig):
        return self.signature_history.count(sig) >= 4

    def store_signature(self, sig):
        self.signature_history.append(sig)
        if len(self.signature_history) > self.sig_max:
            self.signature_history.pop(0)

    # -------------------------
    # MAIN UPDATE
    # -------------------------
    def update(self, sensor, goal):

        if goal:
            self.state = "GOAL_REACHED"
            return

        if self.commit_timer > 0:
            self.commit_timer -= 1
            return

        if self.turn_timer > 0:
            self.turn_timer -= 1
            return

        f = sensor["front"]
        l = sensor["left"]
        r = sensor["right"]

        sig = self.get_signature(sensor)

        # -------------------------
        # NEW: macro-loop detection
        # -------------------------
        if self.repeated_region(sig):
            # force exploration shift
            self.revisit_penalty = 3
        else:
            self.revisit_penalty = max(0, self.revisit_penalty - 1)

        self.store_signature(sig)

        # -------------------------
        # FRONT BLOCK
        # -------------------------
        if f > self.FRONT_BLOCK:
            action = "TURN_RIGHT"

            if self.revisit_penalty > 0:
                action = "TURN_LEFT"

            self.state = action
            self.turn_direction = "RIGHT" if action == "TURN_RIGHT" else "LEFT"
            self.turn_timer = 12
            self.commit_timer = 10
            self.commit_state = action
            return

        # -------------------------
        # SENSOR CLASSIFICATION
        # -------------------------
        left_free = l < self.WALL
        right_free = r < self.WALL

        self.left_free_count = self.left_free_count + 1 if left_free else 0
        self.right_free_count = self.right_free_count + 1 if right_free else 0

        left_ok = self.left_free_count >= 2
        right_ok = self.right_free_count >= 2

        diff = r - l
        self.diff_buffer.append(diff)

        if len(self.diff_buffer) > 7:
            self.diff_buffer.pop(0)

        avg_diff = sum(self.diff_buffer) / len(self.diff_buffer)

        THRESH = 12

        # -------------------------
        # DECISION
        # -------------------------
        if self.commit_state is None:

            if left_ok and right_ok:

                if avg_diff > THRESH:
                    action = "TURN_RIGHT"
                elif avg_diff < -THRESH:
                    action = "TURN_LEFT"
                else:
                    action = "EXPLORE"

                # NEW: macro-loop override
                if self.revisit_penalty > 0 and action != "EXPLORE":
                    action = "TURN_LEFT" if action == "TURN_RIGHT" else "TURN_RIGHT"

                self.state = action

                if action != "EXPLORE":
                    self.turn_direction = action.replace("TURN_", "")
                    self.turn_timer = 10
                    self.commit_timer = 10
                    self.commit_state = action

                return

            elif left_ok:
                self.state = "TURN_LEFT"
                self.turn_direction = "LEFT"
                self.turn_timer = 10
                self.commit_timer = 10
                self.commit_state = "TURN_LEFT"
                return

            elif right_ok:
                self.state = "TURN_RIGHT"
                self.turn_direction = "RIGHT"
                self.turn_timer = 10
                self.commit_timer = 10
                self.commit_state = "TURN_RIGHT"
                return

        self.state = "EXPLORE"

    def get_state(self):
        return self.state