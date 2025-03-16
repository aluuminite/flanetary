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

    # Calculate the minimum translation distance to separate the planets after collision
    overlap = (p1.radius + p2.radius - distance_val) + 0.5  # Add small buffer to ensure separation

    # Normalize the collision vector
    nx, ny = normalize_vector(dx, dy)

    # Separate the planets
    p1.x -= nx * (overlap / 2)
    p1.y -= ny * (overlap / 2)
    p2.x += nx * (overlap / 2) + 1  # Add 100 to p2's x-coordinate to prevent sticking
    p2.y += ny * (overlap / 2)

    # Calculate relative velocity in terms of the normal direction
    dvx = p1.vx - p2.vx
    dvy = p1.vy - p2.vy
    impact_speed = dvx * nx + dvy * ny

    # If they are moving away from each other, no need to resolve
    if impact_speed > 0:
        return

    # Coefficient of restitution (elasticity)
    restitution = 0.9

    # Calculate impulse scalar
    impulse = -(1 + restitution) * impact_speed / (1 / p1.mass + 1 / p2.mass)

    # Apply impulse to the planets
    p1.vx += (impulse * nx) / p1.mass
    p1.vy += (impulse * ny) / p1.mass
    p2.vx -= (impulse * nx) / p2.mass
    p2.vy -= (impulse * ny) / p2.mass