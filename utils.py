import math

def distance(p1, p2):
    """Calculate distance between two points."""
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

def check_collision(p1, p2):
    """Return True if two planets are colliding or a planet and black hole are colliding."""
    if p1.black_hole and not p2.black_hole:
        # Check if planet collides with black hole using planet's radius and 1/3 of black hole's radius
        distance_to_black_hole = distance(p1, p2)
        return distance_to_black_hole <= (p2.radius + p1.radius / 3)
    elif p2.black_hole and not p1.black_hole:
        # Check if planet collides with black hole using planet's radius and 1/3 of black hole's radius
        distance_to_black_hole = distance(p1, p2)
        return distance_to_black_hole <= (p1.radius + p2.radius / 3)
    else:
        # Check normal collision between two planets
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