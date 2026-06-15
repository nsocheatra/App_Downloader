import customtkinter as ctk
from app.version import VERSION, APP_NAME


class AboutModal(ctk.CTkToplevel):
    def __init__(self, parent, on_check_updates=None):
        super().__init__(parent)

        self.title(f"About {APP_NAME}")
        self.geometry("400x420")
        self.resizable(False, False)

        self.on_check_updates = on_check_updates
        self.transient(parent)
        self.grab_set()

        self.build_ui()

    def build_ui(self):
        logo_frame = ctk.CTkFrame(
            self,
            width=80,
            height=80,
            corner_radius=20,
            fg_color="#1e2a45"
        )
        logo_frame.pack(pady=(32, 12))
        logo_frame.pack_propagate(False)

        ctk.CTkLabel(
            logo_frame,
            text="AD",
            font=("Segoe UI", 28, "bold"),
            text_color="#8b5cf6"
        ).pack(expand=True)

        ctk.CTkLabel(
            self,
            text=APP_NAME,
            font=("Segoe UI", 24, "bold"),
            text_color="#e0e0e0"
        ).pack()

        self.version_label = ctk.CTkLabel(
            self,
            text=f"Version {VERSION}",
            font=("Segoe UI", 13),
            text_color="#64748b"
        )
        self.version_label.pack(pady=(2, 12))

        divider = ctk.CTkFrame(self, height=1, fg_color="#1e2448")
        divider.pack(fill="x", padx=40, pady=8)

        ctk.CTkLabel(
            self,
            text="Built with Python + CustomTkinter + yt-dlp",
            font=("Segoe UI", 12),
            text_color="#c0c0c0"
        ).pack(pady=4)

        ctk.CTkLabel(
            self,
            text="Developed by Socheatra (XiaoPang)",
            font=("Segoe UI", 12, "italic"),
            text_color="#8b5cf6"
        ).pack(pady=4)

        ctk.CTkLabel(
            self,
            text="Safe public video downloader",
            font=("Segoe UI", 12),
            text_color="#22c55e"
        ).pack(pady=2)

        ctk.CTkLabel(
            self,
            text="© 2026 App_Downloader. All rights reserved.",
            font=("Segoe UI", 11),
            text_color="#64748b"
        ).pack(pady=(12, 4))

        ctk.CTkButton(
            self,
            text="Check for Updates",
            height=38,
            corner_radius=10,
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            font=("Segoe UI", 13, "bold"),
            command=self._check_updates
        ).pack(pady=(8, 4))

        ctk.CTkButton(
            self,
            text="Close",
            height=38,
            corner_radius=10,
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=self.destroy
        ).pack(pady=(4, 20))

    def _check_updates(self):
        if self.on_check_updates:
            self.on_check_updates(self.version_label)

    def show_update_available(self, latest_version, download_url):
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "Check for Updates":
                widget.configure(
                    text=f"Download v{latest_version}",
                    fg_color="#22c55e",
                    hover_color="#16a34a",
                    command=lambda: self._open_url(download_url)
                )

    def _open_url(self, url):
        import webbrowser
        webbrowser.open(url)
