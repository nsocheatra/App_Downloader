import customtkinter as ctk
from app.ui.modals.settings_modal import SettingsModal
from app.ui.modals.download_details_modal import DownloadDetailsModal
from app.ui.modals.platform_info_modal import PlatformInfoModal
from app.ui.modals.quality_selector_modal import QualitySelectorModal
from app.ui.modals.error_modal import ErrorModal
from app.ui.modals.about_modal import AboutModal
from app.core.theme_manager import MODERN_THEME


SIDEBAR_ITEMS = [
    ("Home", "⌂"),
    ("Downloads", "⬇"),
    ("History", "⏱"),
    ("Settings", "⚙"),
    ("About", "ℹ"),
]

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


class PlatformCard(ctk.CTkFrame):
    def __init__(self, master, platform, on_select, on_info):
        super().__init__(
            master,
            corner_radius=14,
            fg_color=MODERN_THEME["card"],
            border_width=1,
            border_color=MODERN_THEME["border"]
        )
        self.platform = platform
        self.on_select = on_select
        self.on_info = on_info
        self.is_selected = False
        self.build_card()
        self.bind_hover_events(self)

    def bind_hover_events(self, widget):
        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)
        for child in widget.winfo_children():
            if not isinstance(child, ctk.CTkButton):
                self.bind_hover_events(child)

    def on_enter(self, event):
        if not self.is_selected:
            self.configure(border_color=self.platform["color"], fg_color=MODERN_THEME["card_hover"])

    def on_leave(self, event):
        if not self.is_selected:
            self.configure(border_color=MODERN_THEME["border"], fg_color=MODERN_THEME["card"])

    def build_card(self):
        color = self.platform["color"]

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=14, pady=14)

        icon_frame = ctk.CTkFrame(
            inner,
            width=42,
            height=42,
            corner_radius=10,
            fg_color=color
        )
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)

        ctk.CTkLabel(
            icon_frame,
            text=self.platform["name"][0].upper(),
            font=("Segoe UI", 16, "bold"),
            text_color="#ffffff"
        ).pack(expand=True)

        text_col = ctk.CTkFrame(inner, fg_color="transparent")
        text_col.pack(side="left", fill="x", expand=True, padx=(10, 0))

        ctk.CTkLabel(
            text_col,
            text=self.platform["name"],
            font=("Segoe UI", 13, "bold"),
            text_color="#f1f5f9",
            anchor="w"
        ).pack(anchor="w")

        badge_text = "Supported" if self.platform["supported"] else "Coming Soon"
        badge_color = "#22c55e" if self.platform["supported"] else "#f59e0b"
        ctk.CTkLabel(
            text_col,
            text=badge_text,
            font=("Segoe UI", 10),
            text_color=badge_color,
            anchor="w"
        ).pack(anchor="w")

        btn_col = ctk.CTkFrame(inner, fg_color="transparent")
        btn_col.pack(side="right")

        ctk.CTkButton(
            btn_col,
            text="Select",
            height=28,
            width=64,
            corner_radius=8,
            fg_color=color,
            hover_color=color,
            font=("Segoe UI", 11, "bold"),
            command=lambda: self.on_select(self.platform)
        ).pack(side="top", pady=(0, 3))

        ctk.CTkButton(
            btn_col,
            text="i",
            height=22,
            width=64,
            corner_radius=6,
            fg_color="#1c2140",
            hover_color="#252b50",
            font=("Segoe UI", 11, "bold"),
            text_color="#64748b",
            command=lambda: self.on_info(self.platform)
        ).pack(side="top")

    def set_selected(self, selected):
        self.is_selected = selected
        if selected:
            self.configure(
                border_width=2,
                border_color=self.platform["color"],
                fg_color=MODERN_THEME["card_light"]
            )
        else:
            self.configure(
                border_width=1,
                border_color=MODERN_THEME["border"],
                fg_color=MODERN_THEME["card"]
            )


class ModernView(ctk.CTkFrame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color=MODERN_THEME["background"])
        self.app = app_controller
        self.selected_platform = None
        self.cards = {}
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        sidebar = ctk.CTkFrame(
            self,
            width=200,
            corner_radius=0,
            fg_color=MODERN_THEME["sidebar_bg"]
        )
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(24, 28))

        badge = ctk.CTkFrame(
            logo_frame,
            width=36,
            height=36,
            corner_radius=10,
            fg_color="#8b5cf6"
        )
        badge.pack(side="left")
        badge.pack_propagate(False)

        ctk.CTkLabel(
            badge,
            text="AD",
            font=("Segoe UI", 16, "bold"),
            text_color="#ffffff"
        ).pack(expand=True)

        ctk.CTkLabel(
            logo_frame,
            text="App_Downloader",
            font=("Segoe UI", 16, "bold"),
            text_color="#f1f5f9"
        ).pack(side="left", padx=(10, 0))

        for text, icon in SIDEBAR_ITEMS:
            cmd = self.app.open_settings if text == "Settings" else (
                self.app.open_about if text == "About" else lambda: None
            )
            btn = ctk.CTkButton(
                sidebar,
                text=f"  {icon}  {text}",
                height=40,
                corner_radius=10,
                fg_color="#8b5cf6" if text == "Home" else "transparent",
                text_color="#ffffff" if text == "Home" else "#64748b",
                hover_color="#1a1f3a",
                anchor="w",
                font=("Segoe UI", 13),
                command=cmd
            )
            btn.pack(fill="x", padx=14, pady=3)

        self.mode_btn = ctk.CTkButton(
            sidebar,
            text="  🔄  Classic Mode",
            height=40,
            corner_radius=10,
            fg_color="transparent",
            text_color="#64748b",
            hover_color="#1a1f3a",
            anchor="w",
            font=("Segoe UI", 12),
            command=self.app.switch_ui_mode
        )
        self.mode_btn.pack(side="bottom", fill="x", padx=14, pady=20)

        sidebar_status = ctk.CTkFrame(sidebar, fg_color="transparent")
        sidebar_status.pack(side="bottom", fill="x", padx=14, pady=(0, 16))

        status_dot = ctk.CTkFrame(
            sidebar_status,
            width=8,
            height=8,
            corner_radius=4,
            fg_color="#22c55e"
        )
        status_dot.pack(side="left")

        ctk.CTkLabel(
            sidebar_status,
            text="Ready",
            font=("Segoe UI", 11),
            text_color="#64748b"
        ).pack(side="left", padx=(6, 0))

        content = ctk.CTkScrollableFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)

        header_card = ctk.CTkFrame(content, corner_radius=16, fg_color=MODERN_THEME["card"])
        header_card.grid(row=0, column=0, padx=24, pady=(24, 14), sticky="ew")
        header_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header_card,
            text="Video Downloader Dashboard",
            font=("Segoe UI", 24, "bold"),
            text_color="#f1f5f9"
        ).grid(row=0, column=0, padx=22, pady=20, sticky="w")

        url_card = ctk.CTkFrame(content, corner_radius=16, fg_color=MODERN_THEME["card"])
        url_card.grid(row=1, column=0, padx=24, pady=10, sticky="ew")
        url_card.grid_columnconfigure(0, weight=1)

        url_label = ctk.CTkLabel(
            url_card,
            text="Paste a video URL to get started",
            font=("Segoe UI", 12),
            text_color="#64748b"
        )
        url_label.grid(row=0, column=0, padx=22, pady=(14, 6), sticky="sw")

        url_row = ctk.CTkFrame(url_card, fg_color="transparent")
        url_row.grid(row=1, column=0, padx=22, pady=(0, 10), sticky="ew")
        url_row.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(
            url_row,
            placeholder_text="Paste video URL here...",
            height=46,
            corner_radius=10,
            font=("Segoe UI", 14),
            border_width=1,
            border_color="#1e2448",
            fg_color="#0b0e1a",
            text_color="#f1f5f9",
            placeholder_text_color="#3b4270"
        )
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.paste_btn = ctk.CTkButton(
            url_row,
            text="Paste",
            height=46,
            width=80,
            corner_radius=10,
            fg_color="#1c2140",
            hover_color="#252b50",
            font=("Segoe UI", 13, "bold"),
            command=self.paste_url
        )
        self.paste_btn.grid(row=0, column=1, padx=(0, 8))

        self.detect_btn = ctk.CTkButton(
            url_row,
            text="Detect Platform",
            height=46,
            width=130,
            corner_radius=10,
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            font=("Segoe UI", 13, "bold"),
            command=self.app.detect_platform
        )
        self.detect_btn.grid(row=0, column=2)

        platform_section = ctk.CTkFrame(content, corner_radius=16, fg_color=MODERN_THEME["card"])
        platform_section.grid(row=2, column=0, padx=24, pady=12, sticky="ew")
        platform_section.grid_columnconfigure(0, weight=1)

        platform_header = ctk.CTkFrame(platform_section, fg_color="transparent")
        platform_header.pack(fill="x", padx=20, pady=(14, 6))

        ctk.CTkLabel(
            platform_header,
            text="Platforms",
            font=("Segoe UI", 15, "bold"),
            text_color="#f1f5f9"
        ).pack(side="left")

        grid_wrapper = ctk.CTkFrame(platform_section, fg_color="transparent")
        grid_wrapper.pack(fill="x", padx=14, pady=(4, 16))

        columns = 4
        for index, platform in enumerate(PLATFORMS):
            row = index // columns
            col = index % columns

            card = PlatformCard(
                grid_wrapper,
                platform,
                self.select_platform,
                self.show_platform_info
            )
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.cards[platform["key"]] = card

        for col in range(columns):
            grid_wrapper.grid_columnconfigure(col, weight=1, minsize=180)

        options_section = ctk.CTkFrame(content, corner_radius=16, fg_color=MODERN_THEME["card"])
        options_section.grid(row=3, column=0, padx=24, pady=10, sticky="ew")
        options_section.grid_columnconfigure(2, weight=1)

        quality_frame = ctk.CTkFrame(options_section, fg_color="transparent")
        quality_frame.grid(row=0, column=0, padx=(20, 8), pady=16)

        ctk.CTkLabel(
            quality_frame,
            text="Quality",
            font=("Segoe UI", 11, "bold"),
            text_color="#64748b"
        ).pack(anchor="w", pady=(0, 4))

        self.quality_btn = ctk.CTkButton(
            quality_frame,
            text="Best",
            height=36,
            width=130,
            corner_radius=8,
            fg_color="#1c2140",
            hover_color="#252b50",
            font=("Segoe UI", 13),
            text_color="#f1f5f9",
            command=self.open_quality_selector
        )
        self.quality_btn.pack()

        filetype_frame = ctk.CTkFrame(options_section, fg_color="transparent")
        filetype_frame.grid(row=0, column=1, padx=8, pady=16)

        ctk.CTkLabel(
            filetype_frame,
            text="File Type",
            font=("Segoe UI", 11, "bold"),
            text_color="#64748b"
        ).pack(anchor="w", pady=(0, 4))

        self.filetype_menu = ctk.CTkOptionMenu(
            filetype_frame,
            values=["Video", "Audio"],
            width=110,
            height=36,
            corner_radius=8,
            fg_color="#1c2140",
            button_color="#8b5cf6",
            button_hover_color="#7c3aed",
            dropdown_fg_color="#13172b",
            dropdown_hover_color="#1c2140",
            text_color="#f1f5f9",
            dropdown_text_color="#f1f5f9",
            font=("Segoe UI", 13),
            dropdown_font=("Segoe UI", 13)
        )
        self.filetype_menu.pack()
        self.filetype_menu.set("Video")

        filename_frame = ctk.CTkFrame(options_section, fg_color="transparent")
        filename_frame.grid(row=0, column=2, padx=8, pady=16)

        ctk.CTkLabel(
            filename_frame,
            text="Filename Mode",
            font=("Segoe UI", 11, "bold"),
            text_color="#64748b"
        ).pack(anchor="w", pady=(0, 4))

        self.filename_menu = ctk.CTkOptionMenu(
            filename_frame,
            values=["Original", "Mixed", "Hash"],
            width=120,
            height=36,
            corner_radius=8,
            fg_color="#1c2140",
            button_color="#8b5cf6",
            button_hover_color="#7c3aed",
            dropdown_fg_color="#13172b",
            dropdown_hover_color="#1c2140",
            text_color="#f1f5f9",
            dropdown_text_color="#f1f5f9",
            font=("Segoe UI", 13),
            dropdown_font=("Segoe UI", 13)
        )
        self.filename_menu.pack()
        self.filename_menu.set("Original")

        save_frame = ctk.CTkFrame(options_section, fg_color="transparent")
        save_frame.grid(row=0, column=3, padx=8, pady=16, sticky="ew")

        ctk.CTkLabel(
            save_frame,
            text="Save To",
            font=("Segoe UI", 11, "bold"),
            text_color="#64748b"
        ).pack(anchor="w", pady=(0, 4))

        self.save_entry = ctk.CTkEntry(
            save_frame,
            width=160,
            height=36,
            corner_radius=8,
            fg_color="#0b0e1a",
            border_width=1,
            border_color="#1e2448",
            text_color="#f1f5f9",
            font=("Segoe UI", 12)
        )
        self.save_entry.pack(fill="x")
        self.save_entry.insert(0, "downloads/videos")

        action_section = ctk.CTkFrame(content, corner_radius=16, fg_color=MODERN_THEME["card"])
        action_section.grid(row=4, column=0, padx=24, pady=10, sticky="ew")

        action_inner = ctk.CTkFrame(action_section, fg_color="transparent")
        action_inner.pack(fill="x", padx=20, pady=14)

        self.download_btn = ctk.CTkButton(
            action_inner,
            text="⬇ Download",
            height=44,
            width=150,
            corner_radius=10,
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            font=("Segoe UI", 15, "bold"),
            command=self.app.start_download
        )
        self.download_btn.pack(side="left", padx=(0, 10))

        self.stop_btn = ctk.CTkButton(
            action_inner,
            text="■ Stop",
            height=44,
            width=100,
            corner_radius=10,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            font=("Segoe UI", 14, "bold"),
            command=self.app.cancel_download
        )
        self.stop_btn.pack(side="left", padx=10)

        progress_section = ctk.CTkFrame(content, corner_radius=16, fg_color=MODERN_THEME["card"])
        progress_section.grid(row=5, column=0, padx=24, pady=10, sticky="ew")
        progress_section.grid_columnconfigure(0, weight=1)

        progress_inner = ctk.CTkFrame(progress_section, fg_color="transparent")
        progress_inner.pack(fill="x", padx=20, pady=16)

        self.progress = ctk.CTkProgressBar(
            progress_inner,
            height=8,
            corner_radius=4,
            fg_color="#1e2448",
            progress_color="#8b5cf6"
        )
        self.progress.pack(fill="x")
        self.progress.set(0)

        progress_stats = ctk.CTkFrame(progress_inner, fg_color="transparent")
        progress_stats.pack(fill="x", pady=(8, 0))

        self.status_label = ctk.CTkLabel(
            progress_stats,
            text="Ready",
            font=("Segoe UI", 12),
            text_color="#64748b"
        )
        self.status_label.pack(side="left")

        self.progress_pct = ctk.CTkLabel(
            progress_stats,
            text="",
            font=("Segoe UI", 12, "bold"),
            text_color="#8b5cf6"
        )
        self.progress_pct.pack(side="right")

        bottom_bar = ctk.CTkFrame(content, corner_radius=16, fg_color=MODERN_THEME["card"])
        bottom_bar.grid(row=6, column=0, padx=24, pady=(10, 24), sticky="ew")

        bar_inner = ctk.CTkFrame(bottom_bar, fg_color="transparent")
        bar_inner.pack(fill="x", padx=20, pady=12)

        self.open_btn = ctk.CTkButton(
            bar_inner,
            text="📁 Open Folder",
            height=36,
            width=120,
            corner_radius=8,
            fg_color="#1c2140",
            hover_color="#252b50",
            font=("Segoe UI", 13),
            command=self.app.open_downloads_folder
        )
        self.open_btn.pack(side="left", padx=(0, 8))

        self.clear_btn = ctk.CTkButton(
            bar_inner,
            text="🗑 Clear History",
            height=36,
            width=120,
            corner_radius=8,
            fg_color="#1c2140",
            hover_color="#252b50",
            font=("Segoe UI", 13),
            text_color="#ef4444",
            command=self.app.clear_history
        )
        self.clear_btn.pack(side="left", padx=8)

        bottom_status = ctk.CTkFrame(bar_inner, fg_color="transparent")
        bottom_status.pack(side="right")

        status_indicator = ctk.CTkFrame(
            bottom_status,
            width=8,
            height=8,
            corner_radius=4,
            fg_color="#22c55e"
        )
        status_indicator.pack(side="left")

        ctk.CTkLabel(
            bottom_status,
            text="Ready",
            font=("Segoe UI", 12),
            text_color="#64748b"
        ).pack(side="left", padx=(6, 0))

        history_section = ctk.CTkFrame(content, corner_radius=16, fg_color=MODERN_THEME["card"])
        history_section.grid(row=7, column=0, padx=24, pady=(0, 24), sticky="nsew")
        history_section.grid_columnconfigure(0, weight=1)
        history_section.grid_rowconfigure(1, weight=1)

        history_header = ctk.CTkFrame(history_section, fg_color="transparent")
        history_header.grid(row=0, column=0, padx=20, pady=(14, 6), sticky="ew")

        ctk.CTkLabel(
            history_header,
            text="Download History",
            font=("Segoe UI", 15, "bold"),
            text_color="#f1f5f9"
        ).pack(side="left")

        self.history_table = ctk.CTkScrollableFrame(
            history_section,
            corner_radius=10,
            fg_color="#0b0e1a",
            height=140
        )
        self.history_table.grid(row=1, column=0, padx=20, pady=(4, 16), sticky="nsew")

    def paste_url(self):
        try:
            import pyperclip
            text = pyperclip.paste()
            if text:
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, text)
        except ImportError:
            pass

    def open_quality_selector(self):
        def on_select(value):
            labels = {"2160p": "2160p (4K)", "1440p": "1440p (2K)", "1080p": "1080p (FHD)",
                      "720p": "720p (HD)", "480p": "480p (SD)", "mp3": "Audio (MP3)"}
            self.quality_btn.configure(text=labels.get(value, value))
            self._selected_quality = value

        QualitySelectorModal(self, on_select)

    def get_quality(self):
        return getattr(self, "_selected_quality", "best")

    def get_filename_mode(self):
        mapping = {"Original": "original", "Mixed": "mixed", "Hash": "hash"}
        return mapping.get(self.filename_menu.get(), "original")

    def select_platform(self, platform):
        self.selected_platform = platform
        for key, card in self.cards.items():
            card.set_selected(key == platform["key"])
        self.update_status(f"Selected: {platform['name']}", "#a78bfa")

    def show_platform_info(self, platform):
        PlatformInfoModal(self, platform)

    def update_status(self, text, color="#64748b"):
        self.status_label.configure(text=text, text_color=color)
        if "%" in text:
            self.progress_pct.configure(text=text.split("...")[-1].strip() if "..." in text else "")
        elif "Completed" in text:
            self.progress_pct.configure(text="100%", text_color="#22c55e")
        else:
            self.progress_pct.configure(text="")

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
                text_color="#475569"
            ).pack(pady=20)
            return

        columns = ("Platform", "Title", "Quality", "Status", "Date")
        col_widths = [90, 0, 60, 70, 130]

        header_frame = ctk.CTkFrame(
            self.history_table,
            fg_color="#090c17",
            corner_radius=0,
            height=30
        )
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        h_inner = ctk.CTkFrame(header_frame, fg_color="transparent")
        h_inner.pack(fill="both", expand=True, padx=12)

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
                text_color="#475569",
                anchor="w"
            ).pack(side="left")

        for row_idx, row in enumerate(rows):
            bg = "#0b0e1a" if row_idx % 2 == 0 else "#13172b"
            row_frame = ctk.CTkFrame(
                self.history_table,
                corner_radius=4,
                fg_color=bg,
                height=28
            )
            row_frame.pack(fill="x", pady=1)
            row_frame.pack_propagate(False)

            r_inner = ctk.CTkFrame(row_frame, fg_color="transparent")
            r_inner.pack(fill="both", expand=True, padx=12)

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

                color = "#f1f5f9"
                if idx == 3:
                    color = "#22c55e" if val == "completed" else "#ef4444"

                ctk.CTkLabel(
                    f,
                    text=val,
                    font=("Segoe UI", 11),
                    text_color=color,
                    anchor="w"
                ).pack(side="left")
