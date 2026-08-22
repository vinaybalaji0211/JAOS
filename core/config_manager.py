import json
import os

from pathlib import Path

from logs.logger import logger


class ConfigManager:

    FILE_PATH = "config/settings.json"

    MUTABLE_KEYS = (
        "mode",
        "ai_provider",
    )

    DEFAULT_CONFIG = {

        "jarvis_name": "JARVIS OS",

        "mode": "NORMAL",

        "ai_provider": "NONE"

    }

    @staticmethod
    def _validated_profile_settings_path(profile_settings_path):

        try:
            candidate = Path(profile_settings_path)

        except (TypeError, ValueError, OSError) as error:

            raise ValueError(
                "profile_settings_path must be a valid absolute path"
            ) from error

        if not candidate.is_absolute():

            raise ValueError(
                "profile_settings_path must be an absolute path"
            )

        return candidate

    @staticmethod
    def load_config(profile_settings_path=None):
        """
        Return effective settings without writing any file.

        Repository settings are read-only defaults. When
        profile_settings_path is supplied and exists, its mutable keys
        overlay those defaults. Loading never creates either file.
        """

        if os.path.exists(ConfigManager.FILE_PATH):

            with open(
                    ConfigManager.FILE_PATH,
                    "r",
                    encoding="utf-8") as file:

                config = json.load(file)

        else:

            config = dict(ConfigManager.DEFAULT_CONFIG)

        if profile_settings_path is not None:

            overlay_path = ConfigManager._validated_profile_settings_path(
                profile_settings_path
            )

            if overlay_path.exists():

                with open(
                        overlay_path,
                        "r",
                        encoding="utf-8") as file:

                    overlay = json.load(file)

                for key in ConfigManager.MUTABLE_KEYS:

                    if key in overlay:

                        config[key] = overlay[key]

        logger.info(
            "Configuration loaded."
        )

        return config

    @staticmethod
    def save_config(config, profile_settings_path=None):
        """
        Persist mutable settings to an explicit profile settings path.

        Repository settings are read-only. A mutation without an explicit
        absolute profile target fails closed rather than falling back to
        the repository defaults file.
        """

        if profile_settings_path is None:

            raise ValueError(
                "save_config requires an explicit absolute "
                "profile_settings_path; repository configuration "
                "defaults are read-only"
            )

        overlay_path = ConfigManager._validated_profile_settings_path(
            profile_settings_path
        )

        mutable_config = {
            key: config[key]
            for key in ConfigManager.MUTABLE_KEYS
            if key in config
        }

        overlay_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
                overlay_path,
                "w",
                encoding="utf-8") as file:

            json.dump(
                mutable_config,
                file,
                indent=4
            )

        logger.info(
            "Configuration updated."
        )

        return overlay_path
