class Sensors:
    def __init__(self, robot, ps):
        self.robot = robot
        self.ps = ps

    def read(self):
        values = [p.getValue() for p in self.ps]

        print("RAW:", values)

        # Group sensors (ONLY stable sensors (NO ps5 / back-left))
        front = (values[7] + values[0]) * 0.5
        left = values[6]
        right = values[1]

        return {
            "front": front,
            "left": left,
            "right": right
        }
