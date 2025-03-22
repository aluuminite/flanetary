import pygame
import psutil
import settings

from parse import parse_build_file
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SCALE, WHITE, COLOR, TIME_STEP, G, LOG_TOGGLE
from planet import Planet
from physics import apply_gravity, resolve_collision
from utils import check_collision

# Parse the build.txt file and update settings
parse_build_file("build.txt")

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Planet Simulator")
clock = pygame.time.Clock()

# Create a font for rendering text
font = pygame.font.SysFont(None, 24)

# Initialize the start_ticks variable for elapsed time calculation
start_ticks = pygame.time.get_ticks()  # Get the current time in milliseconds
paused_time = 0  # Track total time spent in pause mode
pause_start_ticks = None  # Track when pause started

# Define some planets for testing
planets = [
    Planet(400, 150, 15, (0, 255, 0), 0.1, 0.1),  # 15 x 10¹² tons
    Planet(410, 200, 15, (255, 255, 0), 0.2, 0.1),  # 25 x 10¹² tons
    Planet(570, 300, 30, (69, 255, 69), 0, 0.1)
]

paused = False  # Pause state

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                if paused:
                    pause_start_ticks = pygame.time.get_ticks()  # Start tracking pause time
                    print("Simulation Paused")
                else:
                    paused_time += pygame.time.get_ticks() - pause_start_ticks  # Accumulate paused time
                    print("Simulation Resumed")

    if not paused:
        # Check collisions and resolve them
        for i, p1 in enumerate(planets):
            for j, p2 in enumerate(planets):
                if i < j and check_collision(p1, p2):
                    if LOG_TOGGLE:
                        print(f"Collision detected between planet {i} and planet {j}!")
                    resolve_collision(p1, p2)

        # Apply gravity between planets
        for i, p1 in enumerate(planets):
            for j, p2 in enumerate(planets):
                if i != j:
                    apply_gravity(p1, p2, TIME_STEP)

        # Update planets' positions
        for planet in planets:
            planet.update()

    # Clear screen and draw planets
    screen.fill(COLOR)
    for planet in planets:
        planet.draw(screen, font)  # Pass the font to the draw function

    # Render timer text (Elapsed time, adjusted for pause)
    elapsed_time = (pygame.time.get_ticks() - start_ticks - paused_time) / 1000
    timer_text = font.render(f"Time: {elapsed_time:.2f}s", True, WHITE)
    screen.blit(timer_text, (SCREEN_WIDTH - 100, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()