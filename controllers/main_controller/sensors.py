from config import FRONT_THRESHOLD, LEFT_THRESHOLD, RIGHT_THRESHOLD

class Sensors:
    def __init__(self, robot, ps):
        self.robot = robot
        self.ps = ps
        
    def read(self):
        values = [sensor.getValue() for sensor in self.ps]

        return {
            "front": max(values[2], values[3]),
            "left": values[0],
            "right": values[5]
        }
    
    def is_front_wall(self):
        """Check if there's a wall in front"""
        return max(self.ps[2].getValue(), self.ps[3].getValue()) > FRONT_THRESHOLD
    
    def is_left_wall(self):
        """Check if there's a wall on left side """
        return self.ps[0].getValue() > LEFT_THRESHOLD
    
    def is_right_wall(self):
        """Check if there's a wall on right side """
        return self.ps[5].getValue() > RIGHT_THRESHOLD

"""# In handle_wall_following() method:
front_left = self.is_wall(2)   # Reads ps2
front_right = self.is_wall(3)  # Reads ps3
left = self.is_wall(0)         # Reads ps0
right = self.is_wall(5)        # Reads ps5
"""