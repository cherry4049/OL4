from config import FRONT_THRESHOLD, LEFT_THRESHOLD, RIGHT_THRESHOLD

class Sensors:
    def __init__(self, robot, ps):
        self.robot = robot
        self.ps = ps
        
    def read(self):
        values = [p.getValue() for p in self.ps]

        print("RAE:", values)

        # Group sensors
        front = (values[7] + values[0]) / 2
        left = (values[6] + values[5]) / 2
        right = (values[1] + values[2]) / 2

        return {
            "front": front,
            "left": left,
            "right": right
        }
