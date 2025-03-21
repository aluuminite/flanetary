from flanetary.planet import MASS_UNIT
from flanetary.settings import LOG_TOGGLE
from settings import G
from utils import distance, normalize_vector
import time  # For collision tracking

# Convert KE to terajoules (TJ)
KE_CONVERSION = 10**12  # Conversion factor for kinetic energy

# Function to calculate the full gravitational force between two planets
def calculate_gravity(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance_val = distance(p1, p2)

    if distance_val == 0:
        return 0, 0  # Prevent division by zero

    # Newton's Law of Universal Gravitation
    force_magnitude = G * (p1.mass * p2.mass) / (distance_val ** 2)

    # Normalize direction and apply force magnitude
    nx, ny = normalize_vector(dx, dy)
    fx = force_magnitude * nx
    fy = force_magnitude * ny
    return fx, fy


def apply_gravity(p1, p2, time_step):
    fx, fy = calculate_gravity(p1, p2)

    # Apply force as acceleration (F = ma)
    p1.vx += (fx / p1.mass) * time_step
    p1.vy += (fy / p1.mass) * time_step
    p2.vx -= (fx / p2.mass) * time_step
    p2.vy -= (fy / p2.mass) * time_step

    # Log gravity application
    if LOG_TOGGLE:
        print(f"Gravity applied:")
        print(f"  Force: ({fx:.6f}, {fy:.6f})")
        print(f"  Planet 1 velocity: ({p1.vx:.6f}, {p1.vy:.6f})")
        print(f"  Planet 2 velocity: ({p2.vx:.6f}, {p2.vy:.6f})\n")


def resolve_collision(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance_val = distance(p1, p2)
    if distance_val == 0:
        return

    # Calculate kinetic energy before impact
    ke1_before = 0.5 * (p1.mass * MASS_UNIT) * (p1.vx ** 2 + p1.vy ** 2)
    ke2_before = 0.5 * (p2.mass * MASS_UNIT) * (p2.vx ** 2 + p2.vy ** 2)
    total_ke_before = ke1_before + ke2_before

    # Calculate separation distance
    overlap = (p1.radius + p2.radius - distance_val) * 1.1  # Add space to prevent sticking
    nx, ny = normalize_vector(dx, dy)

    # Separate the planets
    p1.x -= nx * (overlap * 2)
    p1.y -= ny * (overlap * 2)
    p2.x += nx * (overlap * 2)
    p2.y += ny * (overlap * 2)

    # Relative velocity along the normal
    dvx = p1.vx - p2.vx
    dvy = p1.vy - p2.vy
    impact_speed = dvx * nx + dvy * ny

    # Calculate kinetic energy after impact
    ke1_after = 0.5 * (p1.mass * MASS_UNIT) * (p1.vx ** 2 + p1.vy ** 2)
    ke2_after = 0.5 * (p2.mass * MASS_UNIT) * (p2.vx ** 2 + p2.vy ** 2)
    total_ke_after = ke1_after + ke2_after

    # Coefficient of restitution (elasticity)
    restitution = 1  # Perfectly elastic collision

    # Impulse calculation
    impulse = -(1 + restitution) * impact_speed / (1 / p1.mass + 1 / p2.mass)
    p1.vx += (impulse * nx) / p1.mass
    p1.vy += (impulse * ny) / p1.mass
    p2.vx -= (impulse * nx) / p2.mass
    p2.vy -= (impulse * ny) / p2.mass

    # Log kinetic energy before and after impact
    if LOG_TOGGLE:
        print(f"Collision between planets:")
        print(f"  Planet 1: KE before = {ke1_before / KE_CONVERSION:.6f} TJ, KE after = {ke1_after / KE_CONVERSION:.6f} TJ")
        print(f"  Planet 2: KE before = {ke2_before / KE_CONVERSION:.6f} TJ, KE after = {ke2_after / KE_CONVERSION:.6f} TJ")
        print(f"  Total KE: before = {total_ke_before / KE_CONVERSION:.6f} TJ, after = {total_ke_after / KE_CONVERSION:.6f} TJ\n")

    if impact_speed > 0:
        return  # No collision response needed if already moving apart