import customtkinter as ctk


class DownloadDetailsModal(ctk.CTkToplevel):
    def __init__(self, parent, download_info):
        super().__init__(parent)

        self.title("Download Details")
        self.geometry("520x500")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.info = download_info
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text="Download Details",
            font=("Segoe UI", 22, "bold"),
            text_color="#e0e0e0"
        ).pack(pady=(22, 18))

        thumb_frame = ctk.CTkFrame(self, width=480, height=120, corner_radius=12, fg_color="#1e2a45")
        thumb_frame.pack(padx=30)
        thumb_frame.pack_propagate(False)

        thumb_inner = ctk.CTkFrame(thumb_frame, fg_color="transparent")
        thumb_inner.pack(expand=True, fill="both", padx=16, pady=16)

        placeholder = ctk.CTkFrame(thumb_inner, width=80, height=80, corner_radius=8, fg_color="#2a3a55")
        placeholder.pack(side="left")

        ctk.CTkLabel(
            placeholder,
            text="🎬",
            font=("Segoe UI", 32)
        ).pack(expand=True)

        text_area = ctk.CTkFrame(thumb_inner, fg_color="transparent")
        text_area.pack(side="left", fill="x", expand=True, padx=(12, 0))

        title = self.info.get("title", "Unknown Title")
        ctk.CTkLabel(
            text_area,
            text=title,
            font=("Segoe UI", 15, "bold"),
            text_color="#e0e0e0",
            anchor="w",
            wraplength=320
        ).pack(anchor="w", pady=(0, 4))

        platform = self.info.get("platform", "-")
        ctk.CTkLabel(
            text_area,
            text=f"Platform: {platform}",
            font=("Segoe UI", 12),
            text_color="#8899aa",
            anchor="w"
        ).pack(anchor="w")

        details = ctk.CTkScrollableFrame(self, corner_radius=12, fg_color="transparent", height=180)
        details.pack(fill="x", padx=30, pady=(16, 12))

        fields = [
            ("URL", self.info.get("url", "-")),
            ("Duration", self.info.get("duration", "-")),
            ("Uploader", self.info.get("uploader", "-")),
            ("Upload Date", self.info.get("upload_date", "-")),
            ("View Count", self.info.get("view_count", "-")),
            ("Filename", self.info.get("filename", "-")),
            ("Quality", self.info.get("quality", "-")),
            ("Status", self.info.get("status", "-")),
            ("Date", self.info.get("date", "-")),
        ]

        for label, value in fields:
            row = ctk.CTkFrame(details, fg_color="transparent")
            row.pack(fill="x", pady=3)

            ctk.CTkLabel(
                row,
                text=label,
                font=("Segoe UI", 12, "bold"),
                width=100,
                anchor="w",
                text_color="#64748b"
            ).pack(side="left")

            color = "#4ade80" if label == "Status" and value == "completed" else "#e0e0e0"
            ctk.CTkLabel(
                row,
                text=str(value),
                font=("Segoe UI", 12),
                text_color=color,
                anchor="w",
                wraplength=340
            ).pack(side="left", fill="x", expand=True, padx=(10, 0))

        ctk.CTkButton(
            self,
            text="Close",
            height=40,
            corner_radius=12,
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=self.destroy
        ).pack(pady=(0, 18))
