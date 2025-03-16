from settings import G
from utils import distance, normalize_vector

def calculate_gravity(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance_squared = dx**2 + dy**2
    distance = max(distance_squared ** 0.5, 1)  # Prevent division by zero
    force = G * p1.mass * p2.mass / distance_squared
    return (force * dx / distance, force * dy / distance)

def apply_gravity(p1, p2):
    fx, fy = calculate_gravity(p1, p2)
    p1.vx += fx / p1.mass
    p1.vy += fy / p1.mass

def resolve_collision(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance_val = distance(p1, p2)
    if distance_val == 0:
        return

    overlap = (p1.radius + p2.radius - distance_val) + 0.5
    nx, ny = normalize_vector(dx, dy)
    p1.x -= nx * (overlap / 2)
    p1.y -= ny * (overlap / 2)
    p2.x += nx * (overlap / 2)
    p2.y += ny * (overlap / 2)

    dvx = p1.vx - p2.vx
    dvy = p1.vy - p2.vy
    impact_speed = dvx * nx + dvy * ny

    if impact_speed > 0:
        return

    total_mass = p1.mass + p2.mass
    impulse = (2 * impact_speed) / total_mass
    p1.vx -= impulse * p2.mass * nx
    p1.vy -= impulse * p2.mass * ny
    p2.vx += impulse * p1.mass * nx
    p2.vy += impulse * p1.mass * ny