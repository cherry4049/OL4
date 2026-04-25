# =========================
# SPEEDS (safe & stable)
# =========================
FORWARD_SPEED = 5.2
TURN_SPEED = 3.2
SLIGHT_SPEED_DIFF = 1.2
MAX_SPEED = 6.28  # e-puck limit

# =========================
# FSM STABILITY (IMPORTANT)
# =========================
STUCK_LIMIT = 22
STATE_CONFIRM_COUNT = 8   # stronger than v5 to stop flickering

# =========================
# WALL / OPEN DETECTION (FIXED SCALE)
# Based on your real sensor range (60–200 normal, spikes >900)
# =========================
WALL_THRESHOLD = 110      # was too low in v5
OPEN_THRESHOLD = 160      # clearer separation from wall

# =========================
# AVOID HYSTERESIS (CRITICAL FIX)
# Prevents EXPLORE ↔ AVOID oscillation
# =========================
FRONT_AVOID_ON = 120
FRONT_AVOID_OFF = 95      # wider gap = no flip-flop

# =========================
# ESCAPE / RECOVERY
# =========================
ESCAPE_LIMIT = 10

# =========================
# WALL FOLLOWING (LESS NOISY)
# =========================
WALL_DIFF_SMALL = 30
WALL_DIFF_STRONG = 65
WALL_DEADZONE = 12

# =========================
# GOAL DETECTION (UNCHANGED)
# =========================
GOAL_CONFIRM_TIME = 110

# =========================
# JUNCTION DETECTION (IMPORTANT FIX AREA)
# =========================
SIDE_OPEN = 130   # more tolerant (reduces fake openings)
SIDE_WALL = 180   # separates real wall vs noise

# =========================
# SENSOR SPIKE SAFETY (NEW - IMPORTANT FOR YOUR BUGS)
# =========================
SENSOR_MAX_CLAMP = 400   # anything above is noise spike
SENSOR_MIN_VALID = 40    # ignore extremely low noise values