import customtkinter as ctk
import tkinter as tk
from app.core.platform_detector import detect_platform
from app.ui.modals.platform_info_modal import PlatformInfoModal
from app.ui.modals.quality_selector_modal import QualitySelectorModal
from app.ui.modals.error_modal import ErrorModal
from app.version import VERSION

BG = "#0F172A"
SURFACE = "#1E293B"
SURFACE_HOVER = "#24344D"
PRIMARY = "#2563EB"
PRIMARY_HOVER = "#1d4ed8"
TEXT = "#f1f5f9"
MUTED = "#64748b"
BORDER = "#334155"
DANGER = "#dc2626"
DANGER_HOVER = "#b91c1c"
SUCCESS = "#22c55e"
CARD_RADIUS = 12
INPUT_RADIUS = 10
BTN_RADIUS = 10

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

PLATFORM_SHORT = {
    "tiktok": "TT", "facebook": "FB", "youtube": "YT", "instagram": "IG",
    "pinterest": "PT", "douyin": "DY", "vimeo": "VM", "bilibili": "BL",
    "dailymotion": "DM", "kwai": "KW", "likee": "LK", "twitter": "TW",
    "dramabox": "DB", "shortdrama": "SD", "reelshort": "RS", "youku": "YK",
    "iqiyi": "IQ", "tencent": "TC", "mango": "MG", "sohu": "SH",
    "acfun": "AF", "xigua": "XG", "weibo": "WB", "pear": "PR",
}


class ModernView(ctk.CTkFrame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color=BG)
        self.app = app_controller
        self.selected_platform = None
        self.detected_platform = None
        self.is_downloading = False
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build_topbar()
        content = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)

        self.build_workspace(content)
        self.build_queue_section(content)

    def build_topbar(self):
        bar = ctk.CTkFrame(self, height=48, fg_color=SURFACE, corner_radius=0)
        bar.grid(row=0, column=0, sticky="ew")
        bar.grid_propagate(False)

        inner = ctk.CTkFrame(bar, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20)

        badge = ctk.CTkFrame(inner, width=28, height=28, corner_radius=7, fg_color=PRIMARY)
        badge.pack(side="left")
        badge.pack_propagate(False)
        ctk.CTkLabel(badge, text="AD", font=("Segoe UI", 12, "bold"), text_color="#fff").pack(expand=True)

        ctk.CTkLabel(inner, text="App_Downloader", font=("Segoe UI", 14, "bold"), text_color=TEXT).pack(side="left", padx=(10, 0))

        nav = ctk.CTkFrame(inner, fg_color="transparent")
        nav.pack(side="left", padx=(32, 0))
        for text in ["File", "Tools", "Help"]:
            ctk.CTkButton(nav, text=text, fg_color=SURFACE, text_color=MUTED,
                hover_color=SURFACE_HOVER, font=("Segoe UI", 12), width=50, height=28,
                corner_radius=6, command=lambda t=text: self._on_menu(t)).pack(side="left", padx=2)

        right = ctk.CTkFrame(inner, fg_color="transparent")
        right.pack(side="right")
        ctk.CTkLabel(right, text="v" + VERSION, font=("Segoe UI", 11), text_color=MUTED).pack(side="left", padx=(0, 12))


    def _on_menu(self, item):
        if item == "Tools":
            self.app.open_settings()
        elif item == "Help":
            self.app.open_about()
        elif item == "File":
            self.app.open_downloads_folder()

    def build_workspace(self, parent):
        card = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=CARD_RADIUS)
        card.grid(row=0, column=0, padx=24, pady=(24, 0), sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.grid(row=0, column=0, padx=24, pady=20, sticky="ew")
        inner.grid_columnconfigure(0, weight=1)

        url_frame = ctk.CTkFrame(inner, fg_color="transparent")
        url_frame.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        url_frame.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="Paste video or playlist URL here...",
            height=48,
            corner_radius=INPUT_RADIUS,
            font=("Segoe UI", 14),
            border_width=1,
            border_color=BORDER,
            fg_color=BG,
            text_color=TEXT,
            placeholder_text_color=MUTED
        )
        self.url_entry.grid(row=0, column=0, sticky="ew")
        self.url_entry.bind("<KeyRelease>", self._on_url_change)
        self.url_entry.bind("<<Paste>>", self._on_url_change)

        self.platform_badge = ctk.CTkFrame(url_frame, width=32, height=32, corner_radius=8, fg_color="transparent")
        self.platform_label = ctk.CTkLabel(self.platform_badge, text="", font=("Segoe UI", 11, "bold"), text_color=TEXT)

        config_row = ctk.CTkFrame(inner, fg_color="transparent")
        config_row.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        config_row.grid_columnconfigure(3, weight=1)

        qf = self._config_field(config_row, 0, "Quality")
        self.quality_btn = ctk.CTkButton(
            qf, text="Best", height=38, width=130, corner_radius=8,
            fg_color=BG, hover_color=SURFACE_HOVER, font=("Segoe UI", 13),
            text_color=TEXT, border_width=1, border_color=BORDER,
            command=self.open_quality_selector
        )
        self.quality_btn.pack(fill="x")

        ff = self._config_field(config_row, 1, "Format")
        self.filetype_menu = ctk.CTkOptionMenu(
            ff,
            values=["MP4 Video", "Audio"],
            width=130, height=38, corner_radius=8,
            fg_color=BG, button_color=PRIMARY, button_hover_color=PRIMARY_HOVER,
            dropdown_fg_color=SURFACE, dropdown_hover_color=SURFACE_HOVER,
            text_color=TEXT, dropdown_text_color=TEXT,
            font=("Segoe UI", 13), dropdown_font=("Segoe UI", 13)
        )
        self.filetype_menu.pack(fill="x")
        self.filetype_menu.set("MP4 Video")

        nf = self._config_field(config_row, 2, "Filename")
        self.filename_menu = ctk.CTkOptionMenu(
            nf,
            values=["Original", "Mixed", "Hash"],
            width=110, height=38, corner_radius=8,
            fg_color=BG, button_color=PRIMARY, button_hover_color=PRIMARY_HOVER,
            dropdown_fg_color=SURFACE, dropdown_hover_color=SURFACE_HOVER,
            text_color=TEXT, dropdown_text_color=TEXT,
            font=("Segoe UI", 13), dropdown_font=("Segoe UI", 13)
        )
        self.filename_menu.pack(fill="x")
        self.filename_menu.set("Original")

        sf = self._config_field(config_row, 3, "Save To")
        save_inner = ctk.CTkFrame(sf, fg_color="transparent")
        save_inner.pack(fill="x")
        save_inner.grid_columnconfigure(0, weight=1)
        self.save_entry = ctk.CTkEntry(
            save_inner, height=38, corner_radius=8,
            fg_color=BG, border_width=1, border_color=BORDER,
            text_color=TEXT, font=("Segoe UI", 12)
        )
        self.save_entry.grid(row=0, column=0, sticky="ew")
        self.save_entry.insert(0, self.app.config_manager.get("download_dir"))

        btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        btn_frame.grid_columnconfigure(0, weight=1)

        self.download_btn = ctk.CTkButton(
            btn_frame,
            text="Start Download",
            height=46,
            corner_radius=BTN_RADIUS,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=("Segoe UI", 15, "bold"),
            command=self._on_download_click
        )
        self.download_btn.grid(row=0, column=0, sticky="ew")

        link_frame = ctk.CTkFrame(inner, fg_color="transparent")
        link_frame.grid(row=3, column=0, sticky="w")

        self.platforms_link = ctk.CTkButton(
            link_frame,
            text="+ View Supported Platforms (24)",
            fg_color=BG,
            text_color=PRIMARY,
            hover_color=SURFACE_HOVER,
            font=("Segoe UI", 12, "bold"),
            command=self._show_platforms,
            cursor="hand2",
            width=240,
            height=32,
            corner_radius=8
        )
        self.platforms_link.pack(side="left")

        status_row = ctk.CTkFrame(inner, fg_color="transparent")
        status_row.grid(row=4, column=0, sticky="ew", pady=(8, 0))

        self.status_label = ctk.CTkLabel(
            status_row,
            text="Ready",
            font=("Segoe UI", 12),
            text_color=MUTED
        )
        self.status_label.pack(side="left")

        self.progress_pct = ctk.CTkLabel(
            status_row,
            text="",
            font=("Segoe UI", 12, "bold"),
            text_color=PRIMARY
        )
        self.progress_pct.pack(side="right")

        self.progress = ctk.CTkProgressBar(
            status_row,
            height=6,
            corner_radius=3,
            fg_color=BORDER,
            progress_color=PRIMARY
        )
        self.progress.pack(fill="x", pady=(6, 0))
        self.progress.set(0)

    def _config_field(self, parent, col, label):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=0, column=col, padx=(0, 12), sticky="nsew")
        ctk.CTkLabel(f, text=label, font=("Segoe UI", 11, "bold"), text_color=MUTED, anchor="w").pack(anchor="w", pady=(0, 4))
        return f

    def _on_url_change(self, event=None):
        url = self.url_entry.get().strip()
        if url:
            platform = detect_platform(url, PLATFORMS)
            self.detected_platform = platform
            if platform:
                self.selected_platform = platform
                short = PLATFORM_SHORT.get(platform["key"], platform["name"][:2].upper())
                self.platform_badge.configure(fg_color=platform["color"])
                self.platform_badge.place(in_=self.url_entry, relx=1.0, rely=0.5, x=-40, anchor="e")
                self.platform_label.configure(text=short, text_color="#ffffff")
                self.platform_label.place(in_=self.platform_badge, relx=0.5, rely=0.5, anchor="center")
            else:
                self.selected_platform = None
                self.detected_platform = None
                self.platform_badge.place_forget()
                self.platform_label.place_forget()
        else:
            self.selected_platform = None
            self.detected_platform = None
            self.platform_badge.place_forget()
            self.platform_label.place_forget()

    def _on_download_click(self):
        if self.is_downloading:
            self.app.cancel_download()
        else:
            self.app.start_download()

    def _show_platforms(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Supported Platforms")
        modal.geometry("600x500")
        modal.transient(self)
        modal.grab_set()
        modal.configure(fg_color=BG)

        ctk.CTkLabel(modal, text="Supported Platforms (24)",
            font=("Segoe UI", 18, "bold"), text_color=TEXT).pack(pady=(20, 12))

        scroll = ctk.CTkScrollableFrame(modal, corner_radius=CARD_RADIUS, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        for platform in PLATFORMS:
            row = ctk.CTkFrame(scroll, fg_color=SURFACE, corner_radius=8)
            row.pack(fill="x", pady=3)

            badge = ctk.CTkFrame(row, width=36, height=36, corner_radius=8, fg_color=platform["color"])
            badge.pack(side="left", padx=10, pady=8)
            badge.pack_propagate(False)
            ctk.CTkLabel(badge, text=platform["name"][0].upper(),
                font=("Segoe UI", 14, "bold"), text_color="#fff").pack(expand=True)

            ctk.CTkLabel(row, text=platform["name"],
                font=("Segoe UI", 13, "bold"), text_color=TEXT).pack(side="left", padx=(8, 0))

            status = "Supported" if platform["supported"] else "Coming Soon"
            sc = SUCCESS if platform["supported"] else "#f59e0b"
            ctk.CTkLabel(row, text=status, font=("Segoe UI", 11), text_color=sc).pack(side="right", padx=14)

            ctk.CTkLabel(row, text=", ".join(platform["domains"]),
                font=("Segoe UI", 10), text_color=MUTED).pack(side="right", padx=14)

        ctk.CTkButton(modal, text="Close", height=38, corner_radius=BTN_RADIUS,
            fg_color=MUTED, hover_color="#4b5563",
            command=modal.destroy).pack(pady=(0, 16))

    def build_queue_section(self, parent):
        self.queue_frame = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=CARD_RADIUS)
        self.queue_frame.grid(row=1, column=0, padx=24, pady=(16, 24), sticky="ew")
        self.queue_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self.queue_frame, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=(14, 8), sticky="ew")
        ctk.CTkLabel(header, text="Download History",
            font=("Segoe UI", 15, "bold"), text_color=TEXT).pack(side="left")

        bottom_actions = ctk.CTkFrame(header, fg_color="transparent")
        bottom_actions.pack(side="right")
        ctk.CTkButton(bottom_actions, text="Open Folder", height=32, corner_radius=8,
            fg_color=SURFACE, text_color=MUTED, hover_color=SURFACE_HOVER,
            font=("Segoe UI", 12), command=self.app.open_downloads_folder).pack(side="left", padx=2)
        ctk.CTkButton(bottom_actions, text="Clear History", height=32, corner_radius=8,
            fg_color=SURFACE, text_color=DANGER, hover_color=SURFACE_HOVER,
            font=("Segoe UI", 12), command=self.app.clear_history).pack(side="left", padx=2)

        self.history_table = ctk.CTkScrollableFrame(
            self.queue_frame,
            corner_radius=10,
            fg_color=BG,
            height=180
        )
        self.history_table.grid(row=1, column=0, padx=20, pady=(4, 16), sticky="nsew")

    def paste_url(self):
        try:
            text = self.clipboard_get()
            if text:
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, text)
                self._on_url_change()
        except Exception:
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
        self.detected_platform = platform

    def show_platform_info(self, platform):
        PlatformInfoModal(self, platform)

    def update_status(self, text, color=MUTED):
        self.status_label.configure(text=text, text_color=color)
        if "Completed" in text:
            self.progress_pct.configure(text="100%", text_color=SUCCESS)
        elif "%" in text and "..." in text:
            pct = text.split("...")[0].split()[-1] if "..." in text else ""
            self.progress_pct.configure(text=pct, text_color=PRIMARY)
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
                text="No downloads yet — paste a URL above to get started",
                font=("Segoe UI", 12),
                text_color="#475569"
            ).pack(pady=20)
            return

        columns = ("Platform", "Title", "Quality", "Status", "Date")
        col_widths = [90, 0, 60, 70, 130]

        header_frame = ctk.CTkFrame(self.history_table, fg_color="#090c17", corner_radius=0, height=28)
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
            ctk.CTkLabel(f, text=col_name, font=("Segoe UI", 10, "bold"),
                text_color="#475569", anchor="w").pack(side="left")

        for row_idx, row in enumerate(rows):
            bg = BG if row_idx % 2 == 0 else "#0f1729"
            row_frame = ctk.CTkFrame(self.history_table, corner_radius=4, fg_color=bg, height=26)
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

                color = TEXT
                if idx == 3:
                    color = SUCCESS if val == "completed" else DANGER

                ctk.CTkLabel(f, text=val, font=("Segoe UI", 11),
                    text_color=color, anchor="w").pack(side="left")

    def set_downloading_state(self, active):
        self.is_downloading = active
        if active:
            self.download_btn.configure(
                text="Cancel",
                fg_color=DANGER,
                hover_color=DANGER_HOVER
            )
        else:
            self.download_btn.configure(
                text="Start Download",
                fg_color=PRIMARY,
                hover_color=PRIMARY_HOVER
            )
