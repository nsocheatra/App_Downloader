import sys
import threading
import os
import customtkinter as ctk

from app.core.downloader import Downloader
from app.core.filename_manager import build_filename
from app.core.platform_detector import detect_platform
from app.core.config_manager import ConfigManager
from app.core.update_checker import UpdateChecker
from app.version import VERSION
from app.database.history_db import HistoryDB
from app.utils.logger import setup_logger
from app.utils.file_utils import open_folder

from app.ui.modals.settings_modal import SettingsModal
from app.ui.modals.error_modal import ErrorModal
from app.ui.modals.about_modal import AboutModal
from app.ui.modals.download_complete_modal import DownloadCompleteModal

logger = setup_logger()

PLATFORMS = [
    {"name": "TikTok", "key": "tiktok", "color": "#ff2d55", "domains": ["tiktok.com"], "supported": True},
    {"name": "Facebook", "key": "facebook", "color": "#1877f2", "domains": ["facebook.com", "fb.watch"], "supported": True},
    {"name": "YouTube", "key": "youtube", "color": "#ff0000", "domains": ["youtube.com", "youtu.be"], "supported": True},
    {"name": "Instagram", "key": "instagram", "color": "#c13584", "domains": ["instagram.com"], "supported": True},
    {"name": "Pinterest", "key": "pinterest", "color": "#e60023", "domains": ["pinterest.com", "pin.it"], "supported": True},
    {"name": "Douyin", "key": "douyin", "color": "#111827", "domains": ["douyin.com"], "supported": True},
    {"name": "Vimeo", "key": "vimeo", "color": "#1ab7ea", "domains": ["vimeo.com"], "supported": True},
    {"name": "Bilibili", "key": "bilibili", "color": "#00a1d6", "domains": ["bilibili.com"], "supported": True},
    {"name": "Dailymotion", "key": "dailymotion", "color": "#0066dc", "domains": ["dailymotion.com"], "supported": True},
    {"name": "Kwai", "key": "kwai", "color": "#ff7700", "domains": ["kwai.com"], "supported": True},
    {"name": "Likee", "key": "likee", "color": "#4caf50", "domains": ["likee.com"], "supported": True},
    {"name": "Twitter / X", "key": "twitter", "color": "#1da1f2", "domains": ["twitter.com", "x.com"], "supported": True},
    {"name": "DramaBox", "key": "dramabox", "color": "#a855f7", "domains": ["dramabox.com", "dramaboxdb.com"], "supported": True},
    {"name": "ShortDrama", "key": "shortdrama", "color": "#ec4899", "domains": ["shortdrama.com"], "supported": True},
    {"name": "ReelShort", "key": "reelshort", "color": "#6d28d9", "domains": ["reelshort.com"], "supported": True},
    {"name": "Youku", "key": "youku", "color": "#007ac9", "domains": ["youku.com"], "supported": True},
    {"name": "iQiyi", "key": "iqiyi", "color": "#07c160", "domains": ["iqiyi.com"], "supported": True},
    {"name": "Tencent Video", "key": "tencent", "color": "#ff4d2d", "domains": ["v.qq.com"], "supported": True},
    {"name": "Mango TV", "key": "mango", "color": "#ff8c00", "domains": ["mgtv.com"], "supported": True},
    {"name": "Sohu Video", "key": "sohu", "color": "#d81e06", "domains": ["tv.sohu.com"], "supported": True},
    {"name": "AcFun", "key": "acfun", "color": "#ff4d00", "domains": ["acfun.cn"], "supported": True},
    {"name": "Xigua Video", "key": "xigua", "color": "#fe2c55", "domains": ["xigua.com"], "supported": True},
    {"name": "Weibo", "key": "weibo", "color": "#ff8200", "domains": ["weibo.com"], "supported": True},
    {"name": "Pear Video", "key": "pear", "color": "#00bcd4", "domains": ["pearvideo.com"], "supported": True},
]


class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent, on_close):
        super().__init__(parent)
        self.on_close = on_close

        # Borderless window
        self.overrideredirect(True)

        # Size and Position
        width = 500
        height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.configure(fg_color="#0b0e1a")

        # UI elements
        logo_frame = ctk.CTkFrame(
            self,
            width=70,
            height=70,
            corner_radius=18,
            fg_color="#1e2a45"
        )
        logo_frame.pack(pady=(40, 10))
        logo_frame.pack_propagate(False)

        ctk.CTkLabel(
            logo_frame,
            text="AD",
            font=("Segoe UI", 24, "bold"),
            text_color="#8b5cf6"
        ).pack(expand=True)

        ctk.CTkLabel(
            self,
            text="App_Downloader",
            font=("Segoe UI", 26, "bold"),
            text_color="#f1f5f9"
        ).pack()

        ctk.CTkLabel(
            self,
            text="Developed by Socheatra (XiaoPang)",
            font=("Segoe UI", 12, "italic"),
            text_color="#8b5cf6"
        ).pack(pady=(2, 20))

        self.progress = ctk.CTkProgressBar(
            self,
            width=300,
            height=6,
            corner_radius=3,
            fg_color="#1e2448",
            progress_color="#8b5cf6",
            mode="indeterminate"
        )
        self.progress.pack()
        self.progress.start()

        self.status = ctk.CTkLabel(
            self,
            text="Loading application components...",
            font=("Segoe UI", 11),
            text_color="#64748b"
        )
        self.status.pack(pady=10)

        # Automatically close after 2.5 seconds
        self.after(2500, self.finish)

    def finish(self):
        self.progress.stop()
        self.destroy()
        self.on_close()


class AppDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.withdraw()  # Hide main window during splash screen

        self.title("App_Downloader")
        self.geometry("1200x850")
        self.minsize(1000, 700)

        base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        icon_path = os.path.join(base, "app", "assets", "icons", "logo.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.config_manager = ConfigManager()
        self.history_db = HistoryDB()

        ctk.set_appearance_mode(self.config_manager.get("theme", "dark"))
        ctk.set_default_color_theme("blue")

        self.current_view = None
        self.selected_platform = None
        self.download_thread = None
        self.cancel_flag = False

        self.view_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.view_container.pack(fill="both", expand=True)

        self.show_view(self.config_manager.get("ui_mode", "modern"))

        # Launch splash screen
        SplashScreen(self, self.on_splash_done)

    def on_splash_done(self):
        self.deiconify()  # Show main window
        self._check_updates_on_startup()

    def show_view(self, mode):
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None

        if mode == "classic":
            from app.ui.classic_view import ClassicView
            self.current_view = ClassicView(self.view_container, self)
            self.config_manager.set("ui_mode", "classic")
        else:
            from app.ui.modern_view import ModernView
            self.current_view = ModernView(self.view_container, self)
            self.config_manager.set("ui_mode", "modern")

        self.current_view.pack(fill="both", expand=True)
        self.refresh_history()

    def switch_ui_mode(self):
        current = self.config_manager.get("ui_mode", "modern")
        new_mode = "classic" if current == "modern" else "modern"
        self.show_view(new_mode)

    def get_url(self):
        if hasattr(self.current_view, "url_entry"):
            return self.current_view.url_entry.get().strip()
        return ""

    def get_quality(self):
        if hasattr(self.current_view, "get_quality"):
            return self.current_view.get_quality()
        if hasattr(self.current_view, "quality_menu"):
            return self.current_view.quality_menu.get()
        return "best"

    def get_filename_mode(self):
        if hasattr(self.current_view, "get_filename_mode"):
            return self.current_view.get_filename_mode()
        if hasattr(self.current_view, "filename_menu"):
            return self.current_view.filename_menu.get()
        return "original"

    def get_platform_selection(self):
        if hasattr(self.current_view, "selected_platform"):
            return self.current_view.selected_platform
        return None

    def detect_platform(self):
        url = self.get_url()
        if not url:
            self.update_status("Please paste a URL first", "#f87171")
            return

        platform = detect_platform(url, PLATFORMS)
        if platform:
            self.selected_platform = platform
            if hasattr(self.current_view, "select_platform"):
                self.current_view.select_platform(platform)
            self.update_status(f"Detected: {platform['name']}", "#4ade80")
        else:
            self.selected_platform = None
            self.update_status("Platform not detected", "#f87171")

    def start_download(self):
        url = self.get_url()
        if not url:
            self.update_status("Please paste a URL", "#f87171")
            return

        self.selected_platform = self.get_platform_selection()

        if not self.selected_platform:
            self.detect_platform()
            if not self.selected_platform:
                self.update_status("Could not detect platform. Select one manually.", "#f87171")
                return

        if not self.selected_platform["supported"]:
            self.update_status("This platform is not supported yet", "#f87171")
            return

        is_audio = False
        if hasattr(self.current_view, "filetype_menu"):
            is_audio = self.current_view.filetype_menu.get() == "Audio"

        self.cancel_flag = False
        if hasattr(self.current_view, "progress"):
            self.current_view.progress.configure(mode="indeterminate")
            self.current_view.progress.start()
        self.update_status("Starting download...", "#fbbf24")

        self.download_thread = threading.Thread(target=self.download_worker, args=(url, is_audio))
        self.download_thread.daemon = True
        self.download_thread.start()

    def start_audio_download(self):
        url = self.get_url()
        if not url:
            self.update_status("Please paste a URL", "#f87171")
            return

        self.selected_platform = self.get_platform_selection()
        if not self.selected_platform:
            self.detect_platform()
            if not self.selected_platform:
                self.update_status("Could not detect platform", "#f87171")
                return

        if not self.selected_platform["supported"]:
            self.update_status("This platform is not supported yet", "#f87171")
            return

        self.cancel_flag = False
        if hasattr(self.current_view, "progress"):
            self.current_view.progress.configure(mode="indeterminate")
            self.current_view.progress.start()
        self.update_status("Starting audio download...", "#fbbf24")

        self.download_thread = threading.Thread(target=self.download_worker, args=(url, True))
        self.download_thread.daemon = True
        self.download_thread.start()

    def cancel_download(self):
        self.cancel_flag = True
        self.update_status("Cancelling...", "#f87171")

    def progress_hook(self, d):
        if self.cancel_flag:
            raise Exception("Download cancelled by user")

        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total and total > 0:
                percent = downloaded / total
                if hasattr(self.current_view, "progress") and self.current_view.progress.cget("mode") == "indeterminate":
                    self.current_view.progress.stop()
                    self.current_view.progress.configure(mode="determinate")
                self.current_view.set_progress(percent)
                self.update_status(f"Downloading... {int(percent * 100)}%", "#fbbf24")
        elif d["status"] == "finished":
            if hasattr(self.current_view, "progress") and self.current_view.progress.cget("mode") == "indeterminate":
                self.current_view.progress.stop()
                self.current_view.progress.configure(mode="determinate")
            self.current_view.set_progress(1)
            self.update_status("Processing file...", "#fbbf24")

    def download_worker(self, url, is_audio=False):
        try:
            platform_name = self.selected_platform["name"] if self.selected_platform else "Unknown"
            quality = "mp3" if is_audio else self.get_quality()
            filename_mode = self.get_filename_mode()
            filename_template = build_filename(filename_mode, platform_name, url)

            download_dir = self.config_manager.get("download_dir")
            if is_audio or quality == "mp3":
                download_dir = self.config_manager.get("audio_dir")

            downloader = Downloader(download_dir=download_dir)
            info = downloader.download(
                url=url,
                quality=quality,
                filename_template=filename_template,
                progress_hook=self.progress_hook
            )

            title = info.get("title", "Unknown Title")
            self.update_status(f"Completed: {title}", "#4ade80")
            self.current_view.set_progress(1)

            file_path = info.get("_filename", "")
            if not file_path:
                file_path = os.path.join(download_dir, filename_template.replace("%(title)s", title).replace("%(ext)s", "mp4"))

            if self.config_manager.get("save_history", True):
                self.history_db.add_download(
                    platform=platform_name,
                    url=url,
                    title=title,
                    filename=os.path.basename(file_path),
                    quality=quality,
                    status="completed"
                )
                self.refresh_history()

            if self.config_manager.config.get("show_completion_dialog", True):
                try:
                    DownloadCompleteModal(self, title, file_path)
                except Exception:
                    pass

        except Exception as e:
            if hasattr(self.current_view, "progress"):
                self.current_view.progress.stop()
                self.current_view.progress.configure(mode="determinate")
            err_msg = str(e)
            if "cancelled by user" in err_msg.lower():
                self.update_status("Download cancelled", "#f87171")
            else:
                logger.error(f"Download error: {e}", exc_info=True)
                self.update_status(f"Error: {err_msg[:60]}", "#f87171")
                ErrorModal(self, "Download Failed", err_msg, "Check the URL or try another supported platform.")
            self.current_view.set_progress(0)

    def update_status(self, text, color="#8899aa"):
        if hasattr(self.current_view, "update_status"):
            self.current_view.update_status(text, color)

    def refresh_history(self):
        rows = self.history_db.get_history(limit=50)
        if hasattr(self.current_view, "refresh_history"):
            self.current_view.refresh_history(rows)

    def open_settings(self):
        SettingsModal(self, self.config_manager.config, self.on_settings_save)

    def on_settings_save(self, new_config):
        for key, value in new_config.items():
            self.config_manager.set(key, value)

        theme = self.config_manager.get("theme", "dark")
        ctk.set_appearance_mode(theme)

        current_ui = self.config_manager.get("ui_mode", "modern")
        if current_ui != self.config_manager.config.get("ui_mode"):
            self.show_view(self.config_manager.get("ui_mode", "modern"))
        else:
            self.refresh_history()

    def _check_updates_on_startup(self):
        if self.config_manager.get("check_updates_on_startup", True):
            self.update_status("Checking for updates...", "#8899aa")
            checker = UpdateChecker(on_result=self._on_update_result)
            checker.check()

    def _on_update_result(self, checker):
        if checker.has_update:
            self.after(0, lambda: self._show_update_notification(checker))

    def _show_update_notification(self, checker):
        self.update_status(f"Update v{checker.latest_version} available", "#22c55e")
        app = self

        class UpdateNotification(ctk.CTkToplevel):
            def __init__(self):
                super().__init__(app)
                self.title("Update Available")
                self.geometry("400x200")
                self.resizable(False, False)
                self.transient(app)
                self.grab_set()

                ctk.CTkLabel(
                    self,
                    text="Update Available",
                    font=("Segoe UI", 20, "bold"),
                    text_color="#e0e0e0"
                ).pack(pady=(24, 8))

                ctk.CTkLabel(
                    self,
                    text=f"Version {checker.latest_version} is now available.",
                    font=("Segoe UI", 13),
                    text_color="#c0c0c0"
                ).pack()

                ctk.CTkLabel(
                    self,
                    text=f"You are currently on version {VERSION}.",
                    font=("Segoe UI", 13),
                    text_color="#64748b"
                ).pack(pady=(0, 16))

                btn_frame = ctk.CTkFrame(self, fg_color="transparent")
                btn_frame.pack()

                ctk.CTkButton(
                    btn_frame,
                    text="Download",
                    height=38,
                    corner_radius=10,
                    fg_color="#22c55e",
                    hover_color="#16a34a",
                    font=("Segoe UI", 13, "bold"),
                    command=lambda: self._open_url(checker.download_url)
                ).pack(side="left", padx=6)

                ctk.CTkButton(
                    btn_frame,
                    text="Later",
                    height=38,
                    corner_radius=10,
                    fg_color="#6b7280",
                    hover_color="#4b5563",
                    command=self.destroy
                ).pack(side="left", padx=6)

            def _open_url(self, url):
                import webbrowser
                webbrowser.open(url)
                self.destroy()

        UpdateNotification()

    def open_about(self):
        modal = AboutModal(self, on_check_updates=self._handle_about_update_check)
        self._about_modal = modal
        modal.focus()

    def _handle_about_update_check(self, version_label):
        version_label.configure(text="Checking...", text_color="#fbbf24")
        checker = UpdateChecker(on_result=lambda c: self.after(0, lambda: self._on_about_update_result(c, version_label)))
        checker.check()

    def _on_about_update_result(self, checker, version_label):
        if checker.has_update:
            version_label.configure(
                text=f"Update v{checker.latest_version} available",
                text_color="#22c55e"
            )
            if hasattr(self, "_about_modal") and self._about_modal.winfo_exists():
                self._about_modal.show_update_available(checker.latest_version, checker.download_url)
        else:
            version_label.configure(text=f"Version {VERSION} (up to date)", text_color="#4ade80")

    def open_downloads_folder(self):
        download_dir = self.config_manager.get("download_dir")
        open_folder(download_dir)

    def clear_history(self):
        self.history_db.clear_history()
        self.refresh_history()
        self.update_status("History cleared", "#64748b")
