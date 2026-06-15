import customtkinter as ctk


class PlatformInfoModal(ctk.CTkToplevel):
    def __init__(self, parent, platform):
        super().__init__(parent)

        self.title(f"Platform Info - {platform['name']}")
        self.geometry("420x320")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.platform = platform
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text=self.platform["name"],
            font=("Segoe UI", 22, "bold"),
            text_color=self.platform["color"]
        ).pack(pady=(24, 16))

        details = ctk.CTkFrame(self, corner_radius=12, fg_color="transparent")
        details.pack(fill="x", padx=30)

        fields = [
            ("Supported", "Yes" if self.platform.get("supported") else "No"),
            ("Domains", ", ".join(self.platform.get("domains", []))),
            ("Engine", "yt-dlp" if self.platform.get("supported") else "Not Supported"),
        ]

        for label, value in fields:
            row = ctk.CTkFrame(details, fg_color="transparent")
            row.pack(fill="x", pady=6)

            ctk.CTkLabel(
                row,
                text=label,
                font=("Segoe UI", 13, "bold"),
                width=100,
                anchor="w",
                text_color="#8899aa"
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=value,
                font=("Segoe UI", 13),
                text_color="#e0e0e0",
                anchor="w"
            ).pack(side="left", padx=(10, 0))

        if not self.platform.get("supported"):
            note = ctk.CTkTextbox(self, height=60, corner_radius=12, fg_color="#1e2a45")
            note.pack(fill="x", padx=30, pady=16)
            note.insert("0.0", "This platform is not supported by default.\nCreate a custom plugin only if downloads are allowed by the platform.")
            note.configure(state="disabled")

        ctk.CTkButton(
            self,
            text="Close",
            height=40,
            corner_radius=12,
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=self.destroy
        ).pack(pady=(0, 20))
