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
        self.check_error = None

    def check(self):
        thread = threading.Thread(target=self._check_worker, daemon=True)
        thread.start()

    def _parse_version(self, v_str):
        match = re.search(r"[\d.]+", v_str)
        return match.group(0) if match else ""

    def _version_tuple(self, v):
        parts = v.split(".")
        nums = []
        for p in parts:
            try:
                nums.append(int(p))
            except ValueError:
                m = re.match(r"(\d+)", p)
                nums.append(int(m.group(1)) if m else 0)
        return tuple(nums)

    def _check_worker(self):
        try:
            self._check_via_api()
        except Exception as e:
            try:
                self._check_via_raw()
            except Exception as e2:
                self.latest_version = None
                self.has_update = False
                self.check_error = f"{e}\nFallback: {e2}"

        if self.on_result:
            self.on_result(self)

    def _check_via_api(self):
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
        headers = {"User-Agent": f"{APP_NAME}/{VERSION}"}
        resp = requests.get(url, timeout=10, headers=headers)
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
        if not self.exe_download_url:
            for asset in data.get("assets", []):
                if asset["name"].endswith(".exe"):
                    self.exe_download_url = asset["browser_download_url"]
                    break

        self.has_update = self._version_tuple(self.latest_version) > self._version_tuple(VERSION)

    def _check_via_raw(self):
        headers = {"User-Agent": f"{APP_NAME}/{VERSION}"}

        url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/app/version.py"
        resp = requests.get(url, timeout=10, headers=headers)
        if resp.status_code != 200:
            raise Exception(f"Raw fetch returned {resp.status_code}")

        match = re.search(r'VERSION\s*=\s*"([\d.]+)"', resp.text)
        if not match:
            raise Exception("Could not parse version from raw file")

        self.latest_version = match.group(1)
        tag = f"v{self.latest_version}"
        self.download_url = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/tag/{tag}"
        self.exe_download_url = None

        try:
            tag_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/tags/{tag}"
            tag_resp = requests.get(tag_url, timeout=10, headers=headers)
            if tag_resp.status_code == 200:
                tag_data = tag_resp.json()
                for asset in tag_data.get("assets", []):
                    if asset["name"].endswith(".exe"):
                        self.exe_download_url = asset["browser_download_url"]
                        break
        except:
            pass

        if not self.exe_download_url:
            self.exe_download_url = (
                f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/download/"
                f"{tag}/App_Downloader_v{self.latest_version}.exe"
            )
        self.has_update = self._version_tuple(self.latest_version) > self._version_tuple(VERSION)
