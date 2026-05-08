class Sensors:
    def __init__(self, robot, ps, encoders=None):
        self.robot = robot
        self.ps = ps
        self.encoders = encoders  # wheel encoders for motion tracking

    def read(self):
        values = [p.getValue() for p in self.ps]

        front_left = values[7]
        front_right = values[0]

        # Front distance: average of the two forward-facing sensors
        front = (values[7] + values[0]) * 0.5

        left = values[6]
        right = values[1]

        data = {
            "front_left": front_left,
            "front_right": front_right,
            "front": front,
            "left": left,
            "right": right
        }

        # Read encoder positions if available (used for motion tracking)
        if self.encoders:
            left_enc, right_enc = self.encoders
            data["enc_left"] = left_enc.getValue()
            data["enc_right"] = right_enc.getValue()

        return data