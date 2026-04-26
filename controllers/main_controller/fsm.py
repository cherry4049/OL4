class FSM:
    def __init__(self):
        self.state = "EXPLORE"
        self.lock = 0

        # sensor thresholds
        self.OPEN = 180
        self.CLOSE = 450
        self.MARGIN = 20

        # open stability counters
        self.left_open = 0
        self.right_open = 0

        self.initialised = False

        # =========================
        # V6 TURN CONTROL FIX
        # =========================
        self.turn_timer = 0
        self.turn_mode = None   # "LEFT" / "RIGHT"

    def update(self, sensor, goal):

        if goal:
            self.state = "GOAL_REACHED"
            return

        f = sensor["front"]
        l = sensor["left"]
        r = sensor["right"]

        diff = l - r

        # =========================
        # LOCK HANDLING
        # =========================
        if self.lock > 0:
            self.lock -= 1
            return

        # =========================
        # TURN EXECUTION (CRITICAL FIX)
        # =========================
        if self.turn_timer > 0 and self.turn_mode is not None:

            # safety override: if front suddenly blocked, force right turn
            if f > self.CLOSE:
                self.turn_mode = "RIGHT"
                self.state = "TURN_RIGHT"
            else:
                self.state = "TURN_" + self.turn_mode

            self.turn_timer -= 1

            if self.turn_timer <= 0:
                self.turn_mode = None
                self.state = "EXPLORE"

            return

        # =========================
        # EMERGENCY ESCAPE
        # =========================
        if f > self.CLOSE and l > self.CLOSE and r > self.CLOSE:
            self.state = "ESCAPE"
            self.lock = 12
            return

        # =========================
        # FRONT BLOCKED
        # =========================
        if f > 500:
            self.state = "TURN_RIGHT"
            self.turn_mode = "RIGHT"
            self.turn_timer = 10
            return

        # =========================
        # DEAD ZONE FILTER (do NOT force EXPLORE)
        # =========================
        if abs(diff) < self.MARGIN:
            return

        # =========================
        # OPEN SPACE DETECTION
        # =========================
        left_open = l < self.OPEN
        right_open = r < self.OPEN

        if left_open:
            self.left_open += 1
        else:
            self.left_open = 0

        if right_open:
            self.right_open += 1
        else:
            self.right_open = 0

        left_ok = self.left_open >= 4
        right_ok = self.right_open >= 4

        # =========================
        # DECISION RULES (FIXED)
        # =========================
        if not left_ok and not right_ok:
            self.state = "EXPLORE"

        elif left_ok and not right_ok:
            self.state = "TURN_LEFT"
            self.turn_mode = "LEFT"
            self.turn_timer = 8
            self.lock = 0

        elif right_ok and not left_ok:
            self.state = "TURN_RIGHT"
            self.turn_mode = "RIGHT"
            self.turn_timer = 8
            self.lock = 0

        elif left_ok and right_ok:
            # FIX: use difference, not raw comparison
            if (l - r) > 10:
                self.turn_mode = "LEFT"
                self.state = "TURN_LEFT"
            else:
                self.turn_mode = "RIGHT"
                self.state = "TURN_RIGHT"

            self.turn_timer = 12
            self.lock = 0

    def get_state(self):
        return self.state