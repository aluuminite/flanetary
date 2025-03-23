import pygame
import psutil
import settings

from parse import parse_build_file
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SCALE, WHITE, COLOR, TIME_STEP, G, LOG_TOGGLE, RGB_TOGGLE
from planet import Planet
from physics import apply_gravity, resolve_collision
from utils import check_collision, distance

CENTER_X = SCREEN_WIDTH / 2
CENTER_Y = SCREEN_HEIGHT / 2

# Parse the build.txt file and retrieve planet data
planets_data = parse_build_file("build.txt")

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

# Initialize planets dynamically from the parsed build file
planets = planets_data


paused = False  # Pause state

# Initial color
bg_color = list(COLOR)  # Convert tuple to list

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
                    # Update paused time and calculate total elapsed time when resumed
                    paused_time += pygame.time.get_ticks() - pause_start_ticks
                    print("Simulation Resumed")

            # Adjust the background color using hotkeys
            if event.key == pygame.K_r:  # Increase red value
                bg_color[0] = (bg_color[0] + 10) % 256  # Reset to 0 if over 255
                print(f"Updated background color: {bg_color}")
            elif event.key == pygame.K_g:  # Increase green value
                bg_color[1] = (bg_color[1] + 10) % 256  # Reset to 0 if over 255
                print(f"Updated background color: {bg_color}")
            elif event.key == pygame.K_b:  # Increase blue value
                bg_color[2] = (bg_color[2] + 10) % 256  # Reset to 0 if over 255
                print(f"Updated background color: {bg_color}")

            # Increase all color values by 10 when W is pressed
            elif event.key == pygame.K_w:
                bg_color = [(c + 10) % 256 for c in bg_color]
                print(f"Updated background color by 10 to: {bg_color}")

            # Reset all color values to 0 when 0 key is pressed (Black background)
            elif event.key == pygame.K_0:
                bg_color = [0, 0, 0]
                print(f"Reset background color to black: {bg_color}")

            if event.key == pygame.K_i:
                # Set velocity of all planets inward towards the center, excluding black holes
                for planet in planets:
                    if not planet.black_hole:  # Skip black holes
                        dx = CENTER_X - planet.x
                        dy = CENTER_Y - planet.y
                        dist = distance(planet,
                                        Planet(CENTER_X, CENTER_Y, 0, None, 0, 0))  # Use the utils distance function

                        if dist > 0:  # Prevent division by zero if distance is zero
                            norm_dx = dx / dist
                            norm_dy = dy / dist
                            planet.vx = norm_dx * 11  # Adjust speed here as needed
                            planet.vy = norm_dy * 11  # Adjust speed here as needed

            elif event.key == pygame.K_o:
                # Set velocity of all planets outward from the center, excluding black holes
                for planet in planets:
                    if not planet.black_hole:  # Skip black holes
                        dx = planet.x - CENTER_X
                        dy = planet.y - CENTER_Y
                        dist = distance(planet,
                                        Planet(CENTER_X, CENTER_Y, 0, None, 0, 0))  # Use the utils distance function

                        if dist > 0:  # Prevent division by zero if distance is zero
                            norm_dx = dx / dist
                            norm_dy = dy / dist
                            planet.vx = norm_dx * 11  # Adjust speed here as needed
                            planet.vy = norm_dy * 11  # Adjust speed here as needed

    if not paused:
        # Check collisions and resolve them
        for i, p1 in enumerate(planets):
            for j, p2 in enumerate(planets):
                if i < j and check_collision(p1, p2):
                    if LOG_TOGGLE:
                        print(f"Collision detected between planet {i} and planet {j}!")
                    resolve_collision(p1, p2, planets)

        # Apply gravity between planets
        for i, p1 in enumerate(planets):
            for j, p2 in enumerate(planets):
                if i != j:
                    apply_gravity(p1, p2, TIME_STEP)

        # Update planets' positions
        for planet in planets:
            planet.update()

    # Clear screen and draw planets
    screen.fill(bg_color)  # Use the dynamically updated background color
    for planet in planets:
        planet.draw(screen, font)  # Pass the font to the draw function

    # Render timer text (Elapsed time, adjusted for pause), only if not paused
    if not paused:
        elapsed_time = (pygame.time.get_ticks() - start_ticks - paused_time) / 1000
        timer_text = font.render(f"Time: {elapsed_time:.2f}s", True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH - 100, 10))

    # Display RGB values only if RGB_TOGGLE is True
    if RGB_TOGGLE:
        rgb_text = font.render(f"RGB: {bg_color[0]}, {bg_color[1]}, {bg_color[2]}", True, WHITE)
        screen.blit(rgb_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()