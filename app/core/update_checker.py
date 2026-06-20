import re
import threading
import requests
from app.version import VERSION, REPO_OWNER, REPO_NAME


class UpdateChecker:
    def __init__(self, on_result=None):
        self.on_result = on_result
        self.latest_version = None
        self.download_url = None
        self.exe_download_url = None
        self.has_update = False

    def check(self):
        thread = threading.Thread(target=self._check_worker, daemon=True)
        thread.start()

    def _check_worker(self):
        try:
            url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                raise Exception(f"GitHub API returned {resp.status_code}")

            data = resp.json()
            tag = data.get("tag_name", "")
            match = re.search(r"[\d.]+", tag)
            self.latest_version = match.group(0) if match else tag.lstrip("v")
            self.download_url = data.get("html_url", "")

            for asset in data.get("assets", []):
                if asset["name"].endswith(".exe") and "Setup" not in asset["name"]:
                    self.exe_download_url = asset["browser_download_url"]
                    break

            def parse(v):
                return tuple(int(x) for x in v.split("."))

            current = parse(VERSION)
            latest = parse(self.latest_version)
            self.has_update = latest > current

        except Exception:
            self.latest_version = None
            self.has_update = False

        if self.on_result:
            self.on_result(self)
