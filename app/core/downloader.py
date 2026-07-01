import os
import sys
import io
import shutil
import subprocess
import contextlib
import requests
from urllib.parse import urlparse
import yt_dlp


class NullLogger:
    def debug(self, msg):
        pass

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def _has_extractor_for(url):
    try:
        from yt_dlp.extractor import gen_extractors
        for ie in gen_extractors():
            if ie.suitable(url):
                return ie.IE_NAME != "generic"
        return False
    except Exception:
        return False


@contextlib.contextmanager
def _silence_stderr():
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        yield
    finally:
        sys.stderr = old_stderr


class Downloader:
    def __init__(self, download_dir=None, cookies_file=None, cookies_from_browser=None):
        if download_dir is None:
            download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "App_Downloader", "videos")
        self.download_dir = download_dir
        self._ffmpeg_path = None
        self.cookies_file = cookies_file
        self.cookies_from_browser = cookies_from_browser
        try:
            os.makedirs(self.download_dir, exist_ok=True)
        except PermissionError:
            raise PermissionError(
                f"Access denied: Cannot create or access the download folder.\n\n"
                f"Path: {self.download_dir}\n\n"
                "Please check:\n"
                "• The folder is not set to 'Read-only'\n"
                "• You have write permissions for this location\n"
                "• The folder path is valid and not corrupted\n"
                "• Try changing the download location in Settings"
            )

    @staticmethod
    def _get_ffmpeg_path():
        """Locate ffmpeg: check PATH first, then bundled with app, then app data directory."""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            path = shutil.which("ffmpeg")
            if path:
                return path
            return "ffmpeg"
        except Exception:
            pass
        checked = set()
        candidates = []
        if getattr(sys, 'frozen', False):
            meipass = getattr(sys, '_MEIPASS', None)
            if meipass:
                candidates.append(meipass)
            candidates.append(os.path.dirname(sys.executable))
        candidates.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        for base in candidates:
            resolved = os.path.realpath(base)
            if resolved in checked:
                continue
            checked.add(resolved)
            for sub in ["bin", "ffmpeg"]:
                candidate = os.path.join(base, sub, "ffmpeg.exe")
                if os.path.exists(candidate):
                    return candidate
        ffmpeg_dir = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "App_Downloader", "bin")
        ffmpeg_path = os.path.join(ffmpeg_dir, "ffmpeg.exe")
        if os.path.exists(ffmpeg_path):
            return ffmpeg_path
        return None

    @staticmethod
    def _ensure_ffmpeg():
        path = Downloader._get_ffmpeg_path()
        if path:
            try:
                subprocess.run([path, "-version"], capture_output=True, check=True, timeout=10)
                return path
            except Exception:
                if path != "ffmpeg" and os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception:
                        pass
        ffmpeg_dir = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "App_Downloader", "bin")
        os.makedirs(ffmpeg_dir, exist_ok=True)
        ffmpeg_path = os.path.join(ffmpeg_dir, "ffmpeg.exe")
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        zip_path = ffmpeg_path + ".zip"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
        try:
            resp = requests.get(url, headers=headers, timeout=120, stream=True)
            resp.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    if chunk:
                        f.write(chunk)
            import zipfile
            with zipfile.ZipFile(zip_path) as z:
                for name in z.namelist():
                    if name.endswith("ffmpeg.exe"):
                        with z.open(name) as src, open(ffmpeg_path, "wb") as dst:
                            dst.write(src.read())
                        break
            os.remove(zip_path)
            if os.path.exists(ffmpeg_path):
                return ffmpeg_path
        except Exception:
            pass
        return None

    def _build_opts(self, output_path, quality, progress_hook, generic=False):
        ydl_opts = {
            "outtmpl": output_path,
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "logger": NullLogger(),
            "progress_hooks": [progress_hook] if progress_hook else [],
        }

        if generic:
            ydl_opts["force_generic_extractor"] = True

        if self.cookies_file:
            ydl_opts["cookiefile"] = self.cookies_file
        if self.cookies_from_browser:
            ydl_opts["cookiesfrombrowser"] = (self.cookies_from_browser,)

        if self._ffmpeg_path is None:
            self._ffmpeg_path = self._ensure_ffmpeg()
        if self._ffmpeg_path:
            ydl_opts["ffmpeg_location"] = self._ffmpeg_path
            ydl_opts["prefer_ffmpeg"] = True

        has_ffmpeg = bool(self._ffmpeg_path)

        if quality == "best":
            ydl_opts["format"] = "bestvideo+bestaudio/best" if has_ffmpeg else "best"
        elif quality == "1080p":
            ydl_opts["format"] = "bestvideo[height<=1080]+bestaudio/best[height<=1080]" if has_ffmpeg else "best[height<=1080]"
        elif quality == "720p":
            ydl_opts["format"] = "bestvideo[height<=720]+bestaudio/best[height<=720]" if has_ffmpeg else "best[height<=720]"
        elif quality == "480p":
            ydl_opts["format"] = "bestvideo[height<=480]+bestaudio/best[height<=480]" if has_ffmpeg else "best[height<=480]"
        elif quality == "mp3":
            ydl_opts["format"] = "bestaudio/best"
            if has_ffmpeg:
                ydl_opts["postprocessors"] = [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ]
        elif has_ffmpeg:
            ydl_opts["postprocessors"] = [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ]

        return ydl_opts

    def download(self, url, quality="best", filename_template="%(title)s.%(ext)s", progress_hook=None):
        output_path = os.path.join(self.download_dir, filename_template)
        last_error = None

        for use_generic in [False, True]:
            try:
                ydl_opts = self._build_opts(output_path, quality, progress_hook, generic=use_generic)
                with _silence_stderr():
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        return info
            except (yt_dlp.utils.UnsupportedError, yt_dlp.utils.DownloadError) as e:
                last_error = e
                if not use_generic:
                    continue
                has_extractor = _has_extractor_for(url)
                detail = str(e).strip() or "No additional details"
                if "ffmpeg" in detail.lower():
                    error_msg = (
                        f"FFmpeg is required for this download.\n\n"
                        f"Details: {detail}\n\n"
                        "This app uses ffmpeg to merge video and audio streams.\n"
                        "Make sure ffmpeg is installed on your system or bundled correctly.\n"
                        "You can download it from: https://ffmpeg.org/download.html"
                    )
                elif has_extractor:
                    error_msg = (
                        f"Unable to download from this URL.\n\n"
                        f"Details: {detail}\n\n"
                        "Try using a direct video/post URL instead of a profile or playlist page.\n"
                        "If the issue persists, the video may be private, age-restricted,\n"
                        "or require login."
                    )
                else:
                    error_msg = (
                        f"Unsupported platform.\n\n"
                        f"Details: {detail}\n\n"
                        "This platform has no extractor in the download engine.\n"
                        "The site may require login, use JavaScript-based video players,\n"
                        "or have DRM protection that cannot be bypassed."
                    )
                raise ValueError(error_msg)
            except Exception as e:
                last_error = e
                if not use_generic:
                    continue
                raise

        raise last_error or ValueError("Download failed")
