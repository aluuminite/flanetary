# main.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR, TIME_STEP
from planet import Planet
from physics import apply_gravity, resolve_collision
from utils import check_collision

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Planet Simulator")
clock = pygame.time.Clock()

# Create a font for rendering text
font = pygame.font.SysFont(None, 24)

# Initialize the start_ticks variable for elapsed time calculation
start_ticks = pygame.time.get_ticks()  # Get the current time in milliseconds

# Define some planets for testing
planets = [
    Planet(400, 150, 15, (0, 255, 0)),  # 15 x 10¹² tons
    Planet(410, 200, 15, (255, 255, 0))  # 25 x 10¹² tons
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check collisions and resolve them
    for i, p1 in enumerate(planets):
        for j, p2 in enumerate(planets):
            if i < j and check_collision(p1, p2):
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

    # Render timer text (Elapsed time)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer_text = font.render(f"Time: {elapsed_time:.2f}s", True, WHITE)
    screen.blit(timer_text, (SCREEN_WIDTH - 100, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
