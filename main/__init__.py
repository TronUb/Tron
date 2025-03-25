""" Everything starts here """

import os
import platform
from main.others import Colors
from config import Configuration


# Path to check installed Python libraries
INSTALLED_LIBS_FILE = "../installed_requirements.txt"


class Config:
    """Holds dynamically generated configuration values."""


def is_local_host():
    """Check if the script is running locally."""
    return os.path.exists(".env")


class Tools:
    """Handles setup tasks like installing packages and configuring settings."""

    def __init__(self):
        self.device = platform.system().lower()
        self.is_linux = self.device == "linux"
        self.is_windows = self.device == "windows"

    def clear_screen(self):
        """Clear terminal screen based on OS."""
        os.system("clear" if self.is_linux else "cls")

    def setup_config(self):
        """Read configuration from file and set attributes dynamically."""
        count = 1
        self.clear_screen

        config_file = ".env"

        if os.path.exists(config_file):
            print(f"{Colors.block}Config file found: Yes{Colors.reset}\n")

            with open(config_file, "r", encoding="utf-8") as f:
                content = [line.strip() for line in f.readlines() if line.strip()]

            print(f"{Colors.block}Setting configuration values...{Colors.reset}\n")

            for line in content:
                key, value = line.split("=")
                value = int(value) if value.isdigit() else value

                setattr(Config, key, value)
                print(f"[{count}] Config set: {key} = {value}")
                count += 1

        else:
            print("Config file not found. Exiting...")
            exit(1)

        # Load remaining necessary configuration values
        print(
            f"\n{Colors.block}Setting remaining configuration values...{Colors.reset}\n"
        )

        for attr in dir(Configuration):
            if attr.isupper() and not hasattr(Config, attr):
                value = getattr(Configuration, attr, None)
                setattr(Config, attr, value)
                print(f"[{count}] Config set: {attr} = {value}")
                count += 1

        if (
            input(f"\n{Colors.block}Clear screen? (Y/N): {Colors.reset} ")
            .strip()
            .upper()
            == "Y"
        ):
            self.clear_screen


# Initialize configurations
if is_local_host():
    tools = Tools()
    tools.setup_config()
else:
    print("Running in Docker environment. Applying non-localhost setup...")

    for attr in dir(Configuration):
        if attr.isupper() and not hasattr(Config, attr):
            setattr(Config, attr, getattr(Configuration, attr, None))


# Import and initialize userbot
from main.userbot import app

bot = app.bot

from main.core.filters import gen
