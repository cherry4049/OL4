class FSM:
    def __init__(self):
        # Initial state
        self.state = "MOVE_FORWARD"

    def update(self, sensor_data):
        """
        Update state based on sensor input
        sensor_data: dict with keys 'front', 'left', 'right'
        """

        front = sensor_data.get("front", 0)
        left = sensor_data.get("left", 0)
        right = sensor_data.get("right", 0)

        # TODO: replace thresholds with values from config.py later
        FRONT_THRESHOLD = 80
        SIDE_THRESHOLD = 80

        # Simple wall-following logic
        if front > FRONT_THRESHOLD:
            self.state = "TURN_LEFT"
        elif left < SIDE_THRESHOLD:
            self.state = "TURN_LEFT"
        elif front < FRONT_THRESHOLD:
            self.state = "MOVE_FORWARD"
        else:
            self.state = "TURN_RIGHT"

    def get_action(self):
        """
        Return current action for movement module
        """
        return self.state