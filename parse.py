import os
import logging
from planet import Planet
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK_HOLE_COLOR

# Settings path
SETTINGS_FILE = "settings.py"

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

import random


def parse_build_file(file_path):
    if not os.path.isfile(file_path):
        logging.error(f"{file_path} does not exist! Using default settings.")
        return []

    new_settings = {}
    planets = []
    random_planets = False  # Flag to check if random planets are used

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Skip empty lines or comments

            if line.startswith("color ="):
                try:
                    new_settings['COLOR'] = eval(line.split("=", 1)[1].strip())
                    logging.info(f"Updated color to: {new_settings['COLOR']}")
                except Exception as e:
                    logging.error(f"Invalid color format in build.txt. Using default color. Error: {e}")

            elif line.startswith("tstep ="):
                try:
                    new_settings['TIME_STEP'] = float(line.split("=", 1)[1].strip())
                    logging.info(f"Updated time step to: {new_settings['TIME_STEP']}")
                except ValueError:
                    logging.error("Invalid time step value in build.txt. Using default time step.")

            elif line.startswith("g ="):
                try:
                    new_settings['G'] = float(line.split("=", 1)[1].strip())
                    logging.info(f"Updated gravitational constant to: {new_settings['G']}")
                except ValueError:
                    logging.error("Invalid gravitational constant value in build.txt. Using default gravity.")

            elif line.startswith("log ="):
                try:
                    new_settings['LOG_TOGGLE'] = bool(int(line.split("=", 1)[1].strip()))
                    logging.info(f"Updated log toggle to: {new_settings['LOG_TOGGLE']}")
                except ValueError:
                    logging.error("Invalid log value in build.txt. Using default log toggle.")

            elif line.startswith("rgb ="):
                try:
                    new_settings['RGB_TOGGLE'] = bool(int(line.split("=", 1)[1].strip()))
                    logging.info(f"Updated RGB display toggle to: {new_settings['RGB_TOGGLE']}")
                except ValueError:
                    logging.error("Invalid rgb value in build.txt. Using default setting.")

            elif line.startswith("p(") and line.endswith(")"):
                # Planet data (p())
                try:
                    data = eval(line[1:])  # Extract the tuple part after "p"
                    if len(data) == 6:
                        x, y, mass, color, vx, vy = data
                        planets.append(Planet(x, y, mass, color, vx, vy))
                        logging.info(f"Added planet: {data}")
                except Exception as e:
                    logging.error(f"Invalid planet format: {line}. Error: {e}")

            elif line.startswith("r(") and line.endswith(")"):
                # Random planet generation (r())
                if planets:  # If planets have already been added with p(), skip random
                    logging.error("Cannot use random planet generation (r()) with planets added using p().")
                    continue

                try:
                    data = eval(line[1:])  # Extract the tuple part after "r"
                    if len(data) == 3:
                        num_planets, random_velocity, max_mass = data
                        if num_planets <= 0:
                            logging.error(f"Invalid number of random planets: {num_planets}. Must be positive.")
                            continue

                        # Create random planets
                        for _ in range(num_planets):
                            x = random.randint(0, SCREEN_WIDTH)
                            y = random.randint(0, SCREEN_HEIGHT)
                            mass = random.randint(1, max_mass)  # Random mass for planets, constrained by max_mass
                            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                            if random_velocity:
                                vx = random.uniform(-0.3, 0.3)
                                vy = random.uniform(-0.3, 0.3)
                            else:
                                vx = vy = 0

                            planets.append(Planet(x, y, mass, color, vx, vy))
                            logging.info(f"Added random planet: (x={x}, y={y}, mass={mass}, velocity=({vx}, {vy}))")
                except Exception as e:
                    logging.error(f"Invalid random planet format: {line}. Error: {e}")


            elif line.startswith("sr(") and line.endswith(")"):

                # Seeded random planet generation (sr())
                if planets:  # If planets have already been added with p(), skip random

                    logging.error("Cannot use seeded random planet generation (sr()) with planets added using p().")
                    continue

                try:

                    # Strip off 'sr(' and ')', then evaluate the content inside
                    data = eval(line[3:-1])  # Extract the tuple part after "sr("

                    if len(data) == 5:

                        num_planets, random_velocity, max_mass, pos_seed, mass_seed = data

                        if num_planets <= 0:
                            logging.error(f"Invalid number of random seeded planets: {num_planets}. Must be positive.")
                            continue

                        for _ in range(num_planets):

                            # Determine position based on pos_seed:
                            if pos_seed == -1:

                                # Regular generation (uniform distribution)
                                x = random.randint(0, SCREEN_WIDTH)
                                y = random.randint(0, SCREEN_HEIGHT)

                            elif pos_seed == 0:

                                # Majority near center using a Gaussian distribution
                                x = int(random.gauss(SCREEN_WIDTH / 2, SCREEN_WIDTH / 8))
                                y = int(random.gauss(SCREEN_HEIGHT / 2, SCREEN_HEIGHT / 8))
                                x = max(0, min(SCREEN_WIDTH, x))
                                y = max(0, min(SCREEN_HEIGHT, y))

                            elif pos_seed == 1:

                                # Majority near edge
                                if random.random() < 0.5:
                                    x = random.randint(0, SCREEN_WIDTH // 4)

                                else:
                                    x = random.randint(3 * SCREEN_WIDTH // 4, SCREEN_WIDTH)

                                if random.random() < 0.5:
                                    y = random.randint(0, SCREEN_HEIGHT // 4)

                                else:
                                    y = random.randint(3 * SCREEN_HEIGHT // 4, SCREEN_HEIGHT)

                            else:

                                # Fallback to regular generation if seed is unrecognized
                                x = random.randint(0, SCREEN_WIDTH)
                                y = random.randint(0, SCREEN_HEIGHT)

                            # Determine mass based on mass_seed:
                            if mass_seed == -1:

                                # Regular generation
                                mass = random.randint(10, max_mass)

                            elif mass_seed == 0:

                                # All planets have maximum mass
                                mass = max_mass

                            elif mass_seed == 1:

                                # All planets have minimum mass (10)
                                mass = 10

                            elif mass_seed == 2:

                                # Gaussian distribution for mass
                                mean = (max_mass + 10) / 2
                                sigma = (max_mass - 10) / 4
                                mass = int(random.gauss(mean, sigma))
                                mass = max(10, min(max_mass, mass))

                            elif mass_seed == 3:

                                # Opposite of Gaussian: invert the Gaussian value.
                                mean = (max_mass + 10) / 2
                                sigma = (max_mass - 10) / 4
                                g = int(random.gauss(mean, sigma))
                                mass = max_mass + 10 - g
                                mass = max(10, min(max_mass, mass))

                            else:
                                mass = random.randint(10, max_mass)

                            # Standard color generation:
                            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                            # Velocity assignment:
                            if random_velocity:
                                vx = random.uniform(-0.3, 0.3)
                                vy = random.uniform(-0.3, 0.3)

                            else:
                                vx = vy = 0

                            planets.append(Planet(x, y, mass, color, vx, vy))
                            logging.info(
                                f"Added random seeded planet: (x={x}, y={y}, mass={mass}, velocity=({vx}, {vy}))")

                    else:
                        logging.error("Invalid parameters for sr() - must provide 5 parameters.")

                except Exception as e:
                    logging.error(f"Invalid random seeded planet format: {line}. Error: {e}")

            elif line.startswith("b(") and line.endswith(")"):
                try:
                    data = eval(line[1:])  # Extract the tuple part after "b"
                    if len(data) == 3:
                        x, y, mass = data
                        planets.append(Planet(x, y, mass, BLACK_HOLE_COLOR, 0, 0, black_hole=True))
                        logging.info(f"Added black hole: {data}")
                except Exception as e:
                    logging.error(f"Invalid black hole format: {line}. Error: {e}")


        # Update settings.py with new values
        update_settings_file(new_settings)

    except Exception as e:
        logging.error(f"Error parsing file: {e}")

    return planets  # Return parsed planets list



def update_settings_file(new_settings):
    """Write updated settings into settings.py."""
    try:
        with open(SETTINGS_FILE, "r") as file:
            lines = file.readlines()

        with open(SETTINGS_FILE, "w") as file:
            for line in lines:
                # Replace only the values that were updated
                if line.startswith("COLOR") and "COLOR" in new_settings:
                    file.write(f"COLOR = {new_settings['COLOR']}\n")
                elif line.startswith("TIME_STEP") and "TIME_STEP" in new_settings:
                    file.write(f"TIME_STEP = {new_settings['TIME_STEP']}\n")
                elif line.startswith("G =") and "G" in new_settings:
                    file.write(f"G = {new_settings['G']}\n")
                elif line.startswith("LOG_TOGGLE") and "LOG_TOGGLE" in new_settings:
                    file.write(f"LOG_TOGGLE = {new_settings['LOG_TOGGLE']}\n")
                elif line.startswith("RGB_TOGGLE") and "RGB_TOGGLE" in new_settings:
                    file.write(f"RGB_TOGGLE = {new_settings['RGB_TOGGLE']}\n")
                else:
                    file.write(line)  # Keep the line unchanged if it's not being updated

        logging.info("settings.py successfully updated.")

    except Exception as e:
        logging.error(f"Failed to update settings.py: {e}")
