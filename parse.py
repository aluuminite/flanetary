# parse.py
import os
import logging

# Settings path
SETTINGS_FILE = "settings.py"

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_build_file(file_path):

    if not os.path.isfile(file_path):
        logging.error(f"{file_path} does not exist! Using default settings.")
        return  # If the file doesn't exist, we keep defaults

    new_settings = {}

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

        # Update settings.py with new values
        update_settings_file(new_settings)

    except Exception as e:
        logging.error(f"Error parsing file: {e}")

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
