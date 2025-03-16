import math

def distance(p1, p2):
    """Calculate distance between two points."""
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

def check_collision(p1, p2):
    """Return True if two planets are colliding."""
    return distance(p1, p2) <= (p1.radius + p2.radius)

def clamp(value, min_value, max_value):
    """Clamp a value between a min and max."""
    return max(min_value, min(value, max_value))

def normalize_vector(dx, dy):
    """Normalize a vector (dx, dy)."""
    magnitude = math.hypot(dx, dy)
    if magnitude == 0:
        return 0, 0
    return dx / magnitude, dy / magnitude