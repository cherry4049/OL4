class FSM:
    def __init__(self):
        self.state = "EXPLORE"
        self.turn_timer = 0

    def update(self, sensor, goal):

        if goal:
            self.state = "GOAL_REACHED"
            return

        if self.turn_timer > 0:
            self.turn_timer -= 1
            return

        f = sensor["front"]

        # ONLY FRONT DECISION (critical simplification)
        if f > 180:
            self.state = "TURN_RIGHT"
            self.turn_timer = 10
            return

        # ESCAPE only when totally trapped
        if f > 250:
            self.state = "ESCAPE"
            self.turn_timer = 15
            return

        self.state = "EXPLORE"

    def get_state(self):
        return self.state