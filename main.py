import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from planet import Planet
from physics import apply_gravity, resolve_collision
from utils import check_collision

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Planet Simulator")
clock = pygame.time.Clock()

# Create a list of planets
planets = [
    Planet(100, 500, 20, (0, 0, 255), 41),
    Planet(460, 300, 55, (255, 255, 255), 100),
    Planet(300, 150, 33, (0, 255, 0), 25),
    Planet(400, 90, 25, (150, 100, 90), 15)
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for collisions first and resolve them
    for i, p1 in enumerate(planets):
        for j, p2 in enumerate(planets):
            if i < j and check_collision(p1, p2):
                print(f"Collision detected between planet {i} and planet {j}!")
                resolve_collision(p1, p2)

    # Apply gravity after collision resolution
    for i, p1 in enumerate(planets):
        for j, p2 in enumerate(planets):
            if i != j:
                apply_gravity(p1, p2)

    # Update positions
    for planet in planets:
        planet.update()

    # Draw everything
    screen.fill(BLACK)
    for planet in planets:
        planet.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()