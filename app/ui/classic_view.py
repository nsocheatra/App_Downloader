import customtkinter as ctk
from app.ui.modals.settings_modal import SettingsModal
from app.ui.modals.about_modal import AboutModal
from app.ui.modals.platform_info_modal import PlatformInfoModal

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


class ClassicView(ctk.CTkFrame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color="#f5f5f5")
        self.app = app_controller
        self.selected_platform = None
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        menubar = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0, height=38)
        menubar.grid(row=0, column=0, sticky="ew")
        menubar.grid_columnconfigure(2, weight=1)

        for i, item in enumerate(["File", "Tools", "Help"]):
            btn = ctk.CTkButton(
                menubar,
                text=item,
                height=30,
                width=60,
                corner_radius=4,
                fg_color="transparent",
                text_color="#374151",
                hover_color="#f3f4f6",
                font=("Segoe UI", 12),
                command={
                    "File": lambda: None,
                    "Tools": self.app.open_settings,
                    "Help": self.app.open_about,
                }.get(item, lambda: None)
            )
            btn.grid(row=0, column=i, padx=(4, 0), pady=4)

        title_bar = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0, height=52)
        title_bar.grid(row=1, column=0, sticky="ew")
        title_bar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            title_bar,
            text="App_Downloader",
            font=("Segoe UI", 20, "bold"),
            text_color="#111827"
        ).pack(side="left", padx=24, pady=12)

        mode_btn = ctk.CTkButton(
            title_bar,
            text="Modern Mode",
            height=32,
            width=110,
            corner_radius=6,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=("Segoe UI", 12, "bold"),
            command=self.app.switch_ui_mode
        )
        mode_btn.pack(side="right", padx=(0, 24), pady=10)

        url_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#ffffff")
        url_card.grid(row=2, column=0, padx=24, pady=(14, 8), sticky="ew")
        url_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            url_card,
            text="URL:",
            font=("Segoe UI", 13, "bold"),
            text_color="#374151"
        ).grid(row=0, column=0, padx=(16, 6), pady=14)

        self.url_entry = ctk.CTkEntry(
            url_card,
            placeholder_text="Paste video URL here...",
            height=38,
            corner_radius=8,
            font=("Segoe UI", 13),
            border_width=1,
            border_color="#d1d5db",
            fg_color="#f9fafb",
            text_color="#111827",
            placeholder_text_color="#9ca3af"
        )
        self.url_entry.grid(row=0, column=1, padx=6, pady=14, sticky="ew")

        self.paste_btn = ctk.CTkButton(
            url_card,
            text="Paste",
            height=38,
            width=70,
            corner_radius=6,
            fg_color="#6b7280",
            hover_color="#4b5563",
            font=("Segoe UI", 12, "bold"),
            command=self.paste_url
        )
        self.paste_btn.grid(row=0, column=2, padx=6, pady=14)

        self.detect_btn = ctk.CTkButton(
            url_card,
            text="Detect Platform",
            height=38,
            width=120,
            corner_radius=6,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=("Segoe UI", 12, "bold"),
            command=self.app.detect_platform
        )
        self.detect_btn.grid(row=0, column=3, padx=(6, 16), pady=14)

        platform_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#ffffff")
        platform_card.grid(row=3, column=0, padx=24, pady=8, sticky="ew")

        ctk.CTkLabel(
            platform_card,
            text="Platform",
            font=("Segoe UI", 12, "bold"),
            text_color="#374151"
        ).pack(anchor="w", padx=16, pady=(10, 6))

        grid_frame = ctk.CTkFrame(platform_card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=12, pady=(0, 12))

        columns = 5
        for index, platform in enumerate(PLATFORMS):
            row = index // columns
            col = index % columns

            btn = ctk.CTkButton(
                grid_frame,
                text=platform["name"],
                fg_color=platform["color"],
                hover_color=platform["color"],
                height=36,
                corner_radius=6,
                font=("Segoe UI", 11, "bold"),
                text_color="#ffffff",
                command=lambda p=platform: self.select_platform(p)
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="ew")

        for col in range(columns):
            grid_frame.grid_columnconfigure(col, weight=1)

        options_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#ffffff")
        options_card.grid(row=4, column=0, padx=24, pady=8, sticky="ew")
        options_card.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(
            options_card,
            text="Quality:",
            font=("Segoe UI", 12, "bold"),
            text_color="#374151"
        ).grid(row=0, column=0, padx=(16, 4), pady=14)

        self.quality_menu = ctk.CTkOptionMenu(
            options_card,
            values=["best", "1080p", "720p", "480p", "mp3"],
            width=100,
            height=34,
            corner_radius=6,
            fg_color="#f3f4f6",
            button_color="#3b82f6",
            button_hover_color="#2563eb",
            text_color="#111827",
            dropdown_fg_color="#ffffff",
            dropdown_hover_color="#f3f4f6",
            dropdown_text_color="#111827",
            font=("Segoe UI", 12)
        )
        self.quality_menu.grid(row=0, column=1, padx=4, pady=14)

        ctk.CTkLabel(
            options_card,
            text="File Type:",
            font=("Segoe UI", 12, "bold"),
            text_color="#374151"
        ).grid(row=0, column=2, padx=(16, 4), pady=14)

        self.filetype_menu = ctk.CTkOptionMenu(
            options_card,
            values=["Video", "Audio"],
            width=90,
            height=34,
            corner_radius=6,
            fg_color="#f3f4f6",
            button_color="#3b82f6",
            button_hover_color="#2563eb",
            text_color="#111827",
            dropdown_fg_color="#ffffff",
            dropdown_hover_color="#f3f4f6",
            dropdown_text_color="#111827",
            font=("Segoe UI", 12)
        )
        self.filetype_menu.grid(row=0, column=3, padx=4, pady=14)

        ctk.CTkLabel(
            options_card,
            text="Filename:",
            font=("Segoe UI", 12, "bold"),
            text_color="#374151"
        ).grid(row=0, column=4, padx=(16, 4), pady=14)

        self.filename_menu = ctk.CTkOptionMenu(
            options_card,
            values=["original", "hash", "mixed"],
            width=100,
            height=34,
            corner_radius=6,
            fg_color="#f3f4f6",
            button_color="#3b82f6",
            button_hover_color="#2563eb",
            text_color="#111827",
            dropdown_fg_color="#ffffff",
            dropdown_hover_color="#f3f4f6",
            dropdown_text_color="#111827",
            font=("Segoe UI", 12)
        )
        self.filename_menu.grid(row=0, column=5, padx=4, pady=14)

        ctk.CTkLabel(
            options_card,
            text="Save To:",
            font=("Segoe UI", 12, "bold"),
            text_color="#374151"
        ).grid(row=0, column=6, padx=(16, 4), pady=14)

        self.save_entry = ctk.CTkEntry(
            options_card,
            width=150,
            height=34,
            corner_radius=6,
            font=("Segoe UI", 11),
            border_width=1,
            border_color="#d1d5db",
            fg_color="#f9fafb",
            text_color="#111827"
        )
        self.save_entry.grid(row=0, column=7, padx=(4, 16), pady=14)
        self.save_entry.insert(0, "downloads/videos")

        action_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#ffffff")
        action_card.grid(row=5, column=0, padx=24, pady=8, sticky="ew")

        self.download_btn = ctk.CTkButton(
            action_card,
            text="Download",
            height=40,
            width=130,
            corner_radius=6,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=("Segoe UI", 14, "bold"),
            command=self.app.start_download
        )
        self.download_btn.pack(side="left", padx=(16, 8), pady=12)

        self.stop_btn = ctk.CTkButton(
            action_card,
            text="Stop",
            height=40,
            width=90,
            corner_radius=6,
            fg_color="#ef4444",
            hover_color="#dc2626",
            font=("Segoe UI", 14, "bold"),
            command=self.app.cancel_download
        )
        self.stop_btn.pack(side="left", padx=8, pady=12)

        progress_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#ffffff")
        progress_card.grid(row=6, column=0, padx=24, pady=8, sticky="ew")
        progress_card.grid_columnconfigure(0, weight=1)

        progress_inner = ctk.CTkFrame(progress_card, fg_color="transparent")
        progress_inner.pack(fill="x", padx=16, pady=14)

        self.status_label = ctk.CTkLabel(
            progress_inner,
            text="Ready",
            font=("Segoe UI", 12),
            text_color="#6b7280"
        )
        self.status_label.pack(anchor="w", pady=(0, 6))

        self.progress = ctk.CTkProgressBar(
            progress_inner,
            height=6,
            corner_radius=3,
            fg_color="#e5e7eb",
            progress_color="#22c55e"
        )
        self.progress.pack(fill="x")
        self.progress.set(0)

        utility_bar = ctk.CTkFrame(self, corner_radius=10, fg_color="#ffffff")
        utility_bar.grid(row=8, column=0, padx=24, pady=(8, 16), sticky="ew")

        self.open_btn = ctk.CTkButton(
            utility_bar,
            text="Open Folder",
            height=34,
            width=110,
            corner_radius=6,
            fg_color="#6b7280",
            hover_color="#4b5563",
            font=("Segoe UI", 12),
            command=self.app.open_downloads_folder
        )
        self.open_btn.pack(side="left", padx=(16, 8), pady=10)

        self.clear_btn = ctk.CTkButton(
            utility_bar,
            text="Clear History",
            height=34,
            width=110,
            corner_radius=6,
            fg_color="#ef4444",
            hover_color="#dc2626",
            font=("Segoe UI", 12),
            text_color="#ffffff",
            command=self.app.clear_history
        )
        self.clear_btn.pack(side="left", padx=8, pady=10)

        history_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#ffffff")
        history_card.grid(row=7, column=0, padx=24, pady=8, sticky="nsew")
        history_card.grid_columnconfigure(0, weight=1)
        history_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            history_card,
            text="Download History",
            font=("Segoe UI", 14, "bold"),
            text_color="#111827"
        ).grid(row=0, column=0, padx=16, pady=(10, 4), sticky="w")

        self.history_table = ctk.CTkScrollableFrame(
            history_card,
            corner_radius=6,
            fg_color="#f9fafb",
            height=140
        )
        self.history_table.grid(row=1, column=0, padx=16, pady=(4, 12), sticky="nsew")

    def paste_url(self):
        try:
            import pyperclip
            text = pyperclip.paste()
            if text:
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, text)
        except ImportError:
            pass

    def select_platform(self, platform):
        self.selected_platform = platform
        self.update_status(f"Selected: {platform['name']}", "#3b82f6")

    def update_status(self, text, color="#6b7280"):
        self.status_label.configure(text=text, text_color=color)

    def set_progress(self, value):
        self.progress.set(value)

    def refresh_history(self, rows):
        for widget in self.history_table.winfo_children():
            widget.destroy()

        if not rows:
            ctk.CTkLabel(
                self.history_table,
                text="No downloads yet",
                font=("Segoe UI", 12),
                text_color="#9ca3af"
            ).pack(pady=20)
            return

        columns = ("Platform", "Title", "Quality", "Status", "Date")
        col_widths = [90, 0, 60, 70, 130]

        header_frame = ctk.CTkFrame(
            self.history_table,
            fg_color="#e5e7eb",
            corner_radius=0,
            height=28
        )
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        h_inner = ctk.CTkFrame(header_frame, fg_color="transparent")
        h_inner.pack(fill="both", expand=True, padx=10)

        for idx, col_name in enumerate(columns):
            f = ctk.CTkFrame(h_inner, fg_color="transparent")
            f.pack(side="left", fill="x", expand=(col_widths[idx] == 0))
            if col_widths[idx] > 0:
                f.configure(width=col_widths[idx])
                f.pack_propagate(False)
            ctk.CTkLabel(
                f,
                text=col_name,
                font=("Segoe UI", 10, "bold"),
                text_color="#6b7280",
                anchor="w"
            ).pack(side="left")

        for row_idx, row in enumerate(rows):
            bg = "#ffffff" if row_idx % 2 == 0 else "#f9fafb"
            row_frame = ctk.CTkFrame(
                self.history_table,
                corner_radius=2,
                fg_color=bg,
                height=26
            )
            row_frame.pack(fill="x", pady=1)
            row_frame.pack_propagate(False)

            r_inner = ctk.CTkFrame(row_frame, fg_color="transparent")
            r_inner.pack(fill="both", expand=True, padx=10)

            display = (
                str(row[1]) if row[1] else "-",
                str(row[3]) if row[3] else "-",
                str(row[5]) if row[5] else "-",
                str(row[6]) if row[6] else "-",
                str(row[7]) if row[7] else "-",
            )

            for idx, val in enumerate(display):
                f = ctk.CTkFrame(r_inner, fg_color="transparent")
                f.pack(side="left", fill="x", expand=(col_widths[idx] == 0))
                if col_widths[idx] > 0:
                    f.configure(width=col_widths[idx])
                    f.pack_propagate(False)

                color = "#374151"
                if idx == 3:
                    color = "#22c55e" if val == "completed" else "#ef4444"

                ctk.CTkLabel(
                    f,
                    text=val,
                    font=("Segoe UI", 11),
                    text_color=color,
                    anchor="w"
                ).pack(side="left")
