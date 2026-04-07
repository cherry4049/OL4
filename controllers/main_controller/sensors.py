class Sensors:
    def __init__(self, robot, ps):
        self.robot = robot
        self.ps = ps

    def read(self):
        values = [p.getValue() for p in self.ps]

        print("RAW:", values)

        # Group sensors
        front = (values[7] + values[0]) * 0.5
        left = (values[6] + values[5]) * 0.5
        right = (values[1] + values[2]) * 0.5

        return {
            "front": front,
            "left": left,
            "right": right
        }
