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

    def _parse_version(self, v_str):
        match = re.search(r"[\d.]+", v_str)
        return match.group(0) if match else ""

    def _version_tuple(self, v):
        return tuple(int(x) for x in v.split("."))

    def _check_worker(self):
        try:
            self._check_via_api()
        except Exception:
            try:
                self._check_via_raw()
            except Exception:
                self.latest_version = None
                self.has_update = False

        if self.on_result:
            self.on_result(self)

    def _check_via_api(self):
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            raise Exception(f"API returned {resp.status_code}")

        data = resp.json()
        tag = data.get("tag_name", "")
        self.latest_version = self._parse_version(tag) or tag.lstrip("v")
        self.download_url = data.get("html_url", "")
        self.exe_download_url = None

        for asset in data.get("assets", []):
            if asset["name"].endswith(".exe") and "Setup" not in asset["name"]:
                self.exe_download_url = asset["browser_download_url"]
                break

        self.has_update = self._version_tuple(self.latest_version) > self._version_tuple(VERSION)

    def _check_via_raw(self):
        url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/app/version.py"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            raise Exception(f"Raw fetch returned {resp.status_code}")

        match = re.search(r'VERSION\s*=\s*"([\d.]+)"', resp.text)
        if not match:
            raise Exception("Could not parse version from raw file")

        self.latest_version = match.group(1)
        self.download_url = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/tag/v{self.latest_version}"
        self.exe_download_url = (
            f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/download/"
            f"v{self.latest_version}/App_Downloader.exe"
        )
        self.has_update = self._version_tuple(self.latest_version) > self._version_tuple(VERSION)
