class FSM:
    def __init__(self):
        # TODO: define initial state
        self.state = "IDLE"

    def update(self, sensor_data):
        # TODO: state transition logic

        # Example structure:
        # if self.state == "IDLE":
        #     self.state = "MOVE_FORWARD"
        pass

    def get_action(self):
        # TODO: map state → action

        # Example:
        # if self.state == "MOVE_FORWARD":
        #     return "forward"
        return None