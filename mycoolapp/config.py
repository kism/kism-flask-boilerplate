"""Settings Processing."""

import contextlib
import logging
import os
import pwd
import sys

import tomlkit

# This means that the logger will have the right name, loging should be done with this object
logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = {
    "app": {
        "my_message": "Hello, World!",
    },
    "logging": {
        "level": "INFO",
        "path": "",
    },
    "flask": {  # This section is for Flask default config entries https://flask.palletsprojects.com/en/3.0.x/config/
        "DEBUG": False,
    },
}


class MyCoolAppConfig:
    """Object Definition for the settings of the app."""

    def __init__(self) -> None:
        """Init the object with default settings, not much happens."""
        self.settings_path = None

        # Set the variables of this object
        for key, default_value in DEFAULT_SETTINGS.items():
            setattr(self, key, default_value)

    def load_settings_from_disk(self, instance_path: str) -> None:
        """Initiate settings object, get settings from file."""
        # Load the settings from one of the paths

        paths = []
        paths.append(instance_path + os.sep + "settings.toml")
        paths.append(os.path.expanduser("~/.config/mycoolapp/settings.toml"))
        paths.append("/etc/mycoolapp/settings.toml")

        for path in paths:
            if os.path.exists(path):
                logger.info("Found settings at path: %s", path)
                if not self.settings_path:
                    logger.info("Using this path as it's the first one that was found")
                    self.settings_path = path
            else:
                logger.info("No settings file found at: %s", path)

        if not self.settings_path:
            self.settings_path = paths[0]
            logger.critical("No configuration file found, creating at default location: %s", self.settings_path)
            with contextlib.suppress(Exception):
                os.makedirs(instance_path) # Create instance path if it doesn't exist
            self.__write_settings()

        # Load settings file from path
        with open(self.settings_path, encoding="utf8") as toml_file:
            settings_temp = tomlkit.load(toml_file)

        # Set the variables of this object
        for settings_key in DEFAULT_SETTINGS:
            try:
                setattr(self, settings_key, settings_temp[settings_key])
            except (KeyError, TypeError):
                logger.info("%s not defined, leaving as default", settings_key)

        self.__write_settings()

        self.__check_settings()

        logger.info("Config looks all good!")

    def __write_settings(self) -> None:
        """Write settings file."""
        try:
            with open(self.settings_path, "w", encoding="utf8") as toml_file:
                settings_write_temp = vars(self).copy()
                del settings_write_temp["settings_path"]
                tomlkit.dump(settings_write_temp, toml_file)
        except PermissionError as exc:
            user_account = pwd.getpwuid(os.getuid())[0]
            err = f"Fix permissions: chown {user_account} {self.settings_path}"
            raise PermissionError(err) from exc

    def __check_settings(self) -> True:
        """Validate Settings."""
        failure = False

        if failure:
            logger.error("Settings validation failed")
            logger.critical("Exiting")
            sys.exit(1)