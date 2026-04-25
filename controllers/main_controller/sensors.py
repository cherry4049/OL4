class Sensors:
    def __init__(self, robot, ps):
        self.ps = ps
        self.prev = [0.0] * 8
        self.alpha = 0.35

    def clean(self, v):
        return min(v, 800)  # prevent IR explosion

    def read(self):
        raw = [self.clean(p.getValue()) for p in self.ps]

        # EMA smoothing
        smooth = []
        for i in range(8):
            v = self.alpha * raw[i] + (1 - self.alpha) * self.prev[i]
            smooth.append(v)
            self.prev[i] = v

        front = (smooth[7] + smooth[0]) * 0.5
        left = smooth[6]
        right = smooth[1]

        return {
            "front": front,
            "left": left,
            "right": right,
            "raw": raw
        }