from controller import Robot

class Sensors:
    def __init__(self, robot, ps):
        self.ps = ps

        self.history = {
            "front": [],
            "left": [],
            "right": []
        }

        self.window = 5
        self.MAX_SENSOR = 300

    def clamp(self, v):
        return min(v, self.MAX_SENSOR)

    def smooth(self, key, value):
        self.history[key].append(value)
        if len(self.history[key]) > self.window:
            self.history[key].pop(0)
        return sum(self.history[key]) / len(self.history[key])

    def read(self):
        raw = [self.clamp(s.getValue()) for s in self.ps]

        front_raw = raw[0]
        left_raw  = raw[5]
        right_raw = raw[7]

        return {
            # smoothed (control signals)
            "front": self.smooth("front", front_raw),
            "left": self.smooth("left", left_raw),
            "right": self.smooth("right", right_raw),

            # raw geometry (NEVER LOST)
            "front_raw": front_raw,
            "left_raw": left_raw,
            "right_raw": right_raw,
            "raw": raw
        }