class Navigator:
    def __init__(self):
        # memory of visited "situations"
        self.memory = {}

        self.cooldown = 25

    def encode(self, sensor):
        """
        Convert environment into a coarse signature.
        This is NOT SLAM — just pattern grouping.
        """
        f = sensor["front"]
        l = sensor["left"]
        r = sensor["right"]

        def bucket(x):
            if x < 90:
                return "CLOSE"
            elif x < 180:
                return "MID"
            else:
                return "OPEN"

        return f"{bucket(f)}-{bucket(l)}-{bucket(r)}"

    def decide(self, sensor, base_state):
        sig = self.encode(sensor)

        # cooldown memory
        if sig in self.memory and self.memory[sig] > 0:
            self.memory[sig] -= 1
            return "EXPLORE"   # avoid repeating decision

        # mark visit
        self.memory[sig] = self.cooldown

        return base_state