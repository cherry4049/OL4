class FSM:
    def __init__(self):
        self.state = "EXPLORE"
        self.lock = 0

        self.OPEN = 180
        self.CLOSE = 450
        self.MARGIN = 20

        self.left_open = 0
        self.right_open = 0

        self.initialised = False

    def update(self, sensor, goal):

        if goal:
            self.state = "GOAL_REACHED"
            return

        if not self.initialised:
            self.left_open = 0
            self.right_open = 0
            self.initialised = True

        if self.lock > 0:
            self.lock -= 1
            return

        f = sensor["front"]
        l = sensor["left"]
        r = sensor["right"]

        diff = l - r

        # -----------------------
        # EMERGENCY ESCAPE
        # -----------------------
        if f > self.CLOSE and l > self.CLOSE and r > self.CLOSE:
            self.state = "ESCAPE"
            self.lock = 12
            return

        # -----------------------
        # FRONT OBSTACLE
        # -----------------------
        if f > 500:
            self.state = "TURN_RIGHT"
            self.lock = 10
            return

        # -----------------------
        # DEAD ZONE FILTER (IMPORTANT FIX)
        # -----------------------
        if abs(diff) < self.MARGIN:
            # environment symmetric → no turning
            self.left_open = 0
            self.right_open = 0
            self.state = "EXPLORE"
            return

        # -----------------------
        # OPEN SPACE DETECTION
        # -----------------------
        left_open = l < self.OPEN
        right_open = r < self.OPEN

        # stable confirmation
        if left_open:
            self.left_open += 1
        else:
            self.left_open = 0

        if right_open:
            self.right_open += 1
        else:
            self.right_open = 0

        left_ok = self.left_open >= 3
        right_ok = self.right_open >= 3

        # -----------------------
        # DECISION RULES
        # -----------------------
        if not left_ok and not right_ok:
            self.state = "EXPLORE"

        elif left_ok and not right_ok:
            self.state = "TURN_LEFT"
            self.lock = 8

        elif right_ok and not left_ok:
            self.state = "TURN_RIGHT"
            self.lock = 8

        elif left_ok and right_ok:
            self.state = "TURN_LEFT"
            self.lock = 10

    def get_state(self):
        return self.state