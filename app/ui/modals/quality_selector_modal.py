import customtkinter as ctk


QUALITY_OPTIONS = [
    {"label": "2160p (4K)", "value": "2160p", "type": "Video", "size": "~2.5 GB"},
    {"label": "1440p (2K)", "value": "1440p", "type": "Video", "size": "~1.2 GB"},
    {"label": "1080p (FHD)", "value": "1080p", "type": "Video", "size": "~500 MB"},
    {"label": "720p (HD)", "value": "720p", "type": "Video", "size": "~250 MB"},
    {"label": "480p (SD)", "value": "480p", "type": "Video", "size": "~120 MB"},
    {"label": "Audio (MP3 192kbps)", "value": "mp3", "type": "Audio", "size": "~8 MB"},
]


class QualitySelectorModal(ctk.CTkToplevel):
    def __init__(self, parent, on_select):
        super().__init__(parent)

        self.title("Select Quality")
        self.geometry("480x440")
        self.resizable(False, False)

        self.on_select = on_select
        self.transient(parent)
        self.grab_set()

        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text="Select Download Quality",
            font=("Segoe UI", 20, "bold"),
            text_color="#e0e0e0"
        ).pack(pady=(22, 16))

        list_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=12,
            fg_color="transparent",
            height=250
        )
        list_frame.pack(fill="x", padx=24, pady=(0, 16))

        header = ctk.CTkFrame(list_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 6))

        for idx, h in enumerate(["Format", "Type", "Size"]):
            w = [180, 80, 100][idx]
            ctk.CTkLabel(
                header,
                text=h,
                font=("Segoe UI", 11, "bold"),
                text_color="#64748b",
                width=w,
                anchor="w"
            ).pack(side="left", padx=(0, 8))

        self.selected_value = None

        for opt in QUALITY_OPTIONS:
            row = ctk.CTkFrame(list_frame, corner_radius=8, fg_color="#1e2a45")
            row.pack(fill="x", pady=3)

            select_btn = ctk.CTkButton(
                row,
                text="Select",
                width=60,
                height=28,
                corner_radius=6,
                fg_color="#8b5cf6",
                hover_color="#7c3aed",
                font=("Segoe UI", 11, "bold"),
                command=lambda o=opt: self.choose(o)
            )
            select_btn.pack(side="right", padx=8, pady=6)

            ctk.CTkLabel(
                row,
                text=opt["label"],
                font=("Segoe UI", 13, "bold"),
                text_color="#e0e0e0",
                width=180,
                anchor="w"
            ).pack(side="left", padx=(12, 8), pady=6)

            type_color = "#3b82f6" if opt["type"] == "Video" else "#f59e0b"
            ctk.CTkLabel(
                row,
                text=opt["type"],
                font=("Segoe UI", 12),
                text_color=type_color,
                width=80,
                anchor="w"
            ).pack(side="left", padx=8, pady=6)

            ctk.CTkLabel(
                row,
                text=opt["size"],
                font=("Segoe UI", 12),
                text_color="#8899aa",
                width=100,
                anchor="w"
            ).pack(side="left", padx=8, pady=6)

        ctk.CTkButton(
            self,
            text="Cancel",
            height=40,
            corner_radius=12,
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=self.destroy
        ).pack(pady=(0, 18))

    def choose(self, opt):
        self.on_select(opt["value"])
        self.destroy()
