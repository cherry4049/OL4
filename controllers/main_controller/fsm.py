from config import FRONT_THRESHOLD, LEFT_THRESHOLD, RIGHT_THRESHOLD

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

        # Stop condition
        if front >200 and left > 150 and right > 150:
            self.state = "STOP"

        # Obstacle ahead
        elif front > FRONT_THRESHOLD:
            self.state = "TURN_LEFT"
        
        # No wall on left -> go find wall
        elif left < LEFT_THRESHOLD:
            self.state = "TURN_LEFT"

        # No wall on right -> adjust
        elif right < RIGHT_THRESHOLD:
            self.state = "TURN_RIGHT"

        # otherwise go forward
        else:
            self.state = "MOVE_FORWARD"

    def get_action(self):
        """
        Return current action for movement module
        """
        return self.state