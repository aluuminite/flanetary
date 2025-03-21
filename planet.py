import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from utils import clamp


DENSITY = 3000  # kg/m³
MASS_UNIT = 10**15  # 10^12 tons in kg

from settings import SCALE

class Planet:
    def __init__(self, x, y, mass, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        # Calculate radius based on mass (with scaling)
        self.radius = ((3 * (mass * MASS_UNIT) / (4 * 3.14159 * DENSITY)) ** (1 / 3)) * SCALE
        self.vx = 0
        self.vy = 0

    def draw(self, screen, font):
        """Draw the planet on the screen and display its mass and radius."""
        # Draw the planet
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

        # Prepare text to display (Mass and Radius)
        mass_text = font.render(f"Mass: {self.mass}^15kg", True, (255, 255, 255))
        radius_text = font.render(f"Radius: {int(self.radius)} km", True, (255, 255, 255))

        # Position text above the planet
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

        # Clamp x and y to prevent them from going out of screen bounds
        self.x = clamp(self.x, 0, SCREEN_WIDTH)
        self.y = clamp(self.y, 0, SCREEN_HEIGHT)