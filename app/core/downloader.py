import os
import sys
import io
import contextlib
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
    def __init__(self, download_dir=None):
        if download_dir is None:
            download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "App_Downloader", "videos")
        self.download_dir = download_dir
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

        if quality == "best":
            ydl_opts["format"] = "bestvideo+bestaudio/best"
        elif quality == "1080p":
            ydl_opts["format"] = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
        elif quality == "720p":
            ydl_opts["format"] = "bestvideo[height<=720]+bestaudio/best[height<=720]"
        elif quality == "480p":
            ydl_opts["format"] = "bestvideo[height<=480]+bestaudio/best[height<=480]"
        elif quality == "mp3":
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
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
                if has_extractor:
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
