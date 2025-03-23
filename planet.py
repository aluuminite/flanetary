import pygame
import math

from flanetary.settings import BLACK_HOLE_COLOR
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from utils import clamp

DENSITY = 3000  # kg/m³
MASS_UNIT = 10**15  # 10^12 tons in kg
from settings import SCALE

class Planet:
    def __init__(self, x, y, mass, color, vx, vy, black_hole=False):
        self.x = x
        self.y = y
        self.mass = mass
        self.color = BLACK_HOLE_COLOR if black_hole else color
        self.radius = 63 if black_hole else ((3 * (mass * MASS_UNIT) / (4 * 3.14159 * DENSITY)) ** (1 / 3)) * SCALE
        print(self.radius)
        self.vx = 0 if black_hole else vx
        self.vy = 0 if black_hole else vy
        self.black_hole = black_hole
        self.time = 0

    def get_animated_color(self):
        """Animate between (252, 249, 149) and (240, 168, 86) using sine wave."""
        t = (math.sin(self.time) + 1) / 2  # Normalize sine wave from -1..1 to 0..1
        r = int(252 * (1 - t) + 240 * t)
        g = int(249 * (1 - t) + 168 * t)
        b = int(149 * (1 - t) + 86 * t)
        return (r, g, b)

    def draw(self, screen, font):
        """Draw planets and black holes with proper rendering."""
        if self.black_hole:
            # Get the pulsating color for black hole
            animated_color = self.get_animated_color()

            # Core black hole
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), int(self.radius))

            # Animated ring around the black hole
            pygame.draw.circle(screen, animated_color, (int(self.x), int(self.y)), int(self.radius * 1.2), 12)

            # Accretion disk settings
            disk_half_width = self.radius * 2.5
            disk_thickness = self.radius * 0.15
            points = []
            num_segments = 50  # Smoothness

            for i in range(num_segments + 1):
                angle = math.pi * (i / num_segments)
                x_offset = math.cos(angle) * disk_half_width
                y_offset = math.sin(angle) ** 2 * disk_thickness
                points.append((self.x - x_offset, self.y - y_offset))

            for i in range(num_segments + 1):
                angle = math.pi * (1 - i / num_segments)
                x_offset = math.cos(angle) * disk_half_width
                y_offset = math.sin(angle) ** 2 * disk_thickness
                points.append((self.x + x_offset, self.y + y_offset))

            # Draw the animated accretion disk
            pygame.draw.polygon(screen, animated_color, points)

            # Labels
            label_text = font.render("Black Hole", True, (255, 255, 255))
            mass_text = font.render(f"Mass: {self.mass}^15kg", True, (255, 255, 255))
            screen.blit(label_text, (int(self.x) - label_text.get_width() // 2, int(self.y) - self.radius - 20))
            screen.blit(mass_text, (int(self.x) - mass_text.get_width() // 2, int(self.y) - self.radius - 40))

        else:
            # 🌍 Draw regular planets
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

            # Labels for regular planets
            mass_text = font.render(f"Mass: {self.mass}^15kg", True, (255, 255, 255))
            radius_text = font.render(f"Radius: {int(self.radius)} km", True, (255, 255, 255))
            screen.blit(mass_text, (int(self.x) - mass_text.get_width() // 2, int(self.y) - self.radius - 20))
            screen.blit(radius_text, (int(self.x) - radius_text.get_width() // 2, int(self.y) - self.radius - 40))

    def calculate_radius(self):
        """Calculate radius based on mass and constant density."""
        volume = self.mass / DENSITY  # Volume = Mass / Density
        radius = (3 * volume / (4 * math.pi)) ** (1 / 3)  # Solve for r
        return max(int(round(radius)), 1)  # Ensure at least 1 pixel radius

    def update(self):
        """Update planet position based on velocity and keep it within screen bounds."""
        self.x += self.vx
        self.y += self.vy
        self.time += 0.01


        # Clamp x and y to prevent them from going out of screen bounds
        self.x = clamp(self.x, 0, SCREEN_WIDTH)
        self.y = clamp(self.y, 0, SCREEN_HEIGHT)
