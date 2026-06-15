import json
import os


DEFAULT_CONFIG = {
    "app_name": "App_Downloader",
    "ui_mode": "modern",
    "theme": "dark",
    "download_dir": "downloads/videos",
    "audio_dir": "downloads/audio",
    "filename_mode": "original",
    "default_quality": "best",
    "max_threads": 2,
    "save_history": True,
    "auto_detect_platform": True,
    "check_updates_on_startup": True,
}


class ConfigManager:
    def __init__(self, config_path=None):
        if config_path is None:
            if os.path.exists("config.json"):
                config_path = "config.json"
            else:
                base = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "App_Downloader")
                config_path = os.path.join(base, "config.json")
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
            except Exception:
                return dict(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    def save_config(self):
        dir_name = os.path.dirname(self.config_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
