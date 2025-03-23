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
        self.radius = ((3 * (mass * MASS_UNIT) / (4 * 3.14159 * DENSITY)) ** (1 / 3)) * SCALE
        self.vx = 0 if black_hole else vx
        self.vy = 0 if black_hole else vy
        self.black_hole = black_hole

    def draw(self, screen, font):
        """Draw the planet or black hole on the screen and display relevant info."""
        if self.black_hole:
            # Black hole is drawn as a black circle with a white outline
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), int(self.radius))  # Core black hole
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), int(self.radius) + 2,
                               1)  # White outline

            # Label it explicitly as a black hole
            label_text = font.render("Black Hole", True, (255, 255, 255))
            mass_text = font.render(f"Mass: {self.mass}^15kg", True, (255, 255, 255))

            screen.blit(label_text, (int(self.x) - label_text.get_width() // 2, int(self.y) - self.radius - 20))
            screen.blit(mass_text, (int(self.x) - mass_text.get_width() // 2, int(self.y) - self.radius - 40))
        else:
            # Regular planet drawing
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
