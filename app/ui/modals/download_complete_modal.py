import customtkinter as ctk
from app.utils.file_utils import open_folder


class DownloadCompleteModal(ctk.CTkToplevel):
    def __init__(self, parent, title, file_path):
        super().__init__(parent)

        self.title("Download Complete")
        self.geometry("400x320")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.file_path = file_path
        self.build_ui(title, file_path)

    def build_ui(self, title, file_path):
        success_circle = ctk.CTkFrame(
            self,
            width=72,
            height=72,
            corner_radius=36,
            fg_color="#065f46"
        )
        success_circle.pack(pady=(28, 12))
        success_circle.pack_propagate(False)

        ctk.CTkLabel(
            success_circle,
            text="✓",
            font=("Segoe UI", 32, "bold"),
            text_color="#22c55e"
        ).pack(expand=True)

        ctk.CTkLabel(
            self,
            text="Download Completed!",
            font=("Segoe UI", 20, "bold"),
            text_color="#22c55e"
        ).pack(pady=(4, 8))

        details = ctk.CTkFrame(self, corner_radius=12, fg_color="#1e2a45")
        details.pack(fill="x", padx=30, pady=8)

        ctk.CTkLabel(
            details,
            text=title,
            font=("Segoe UI", 13, "bold"),
            text_color="#e0e0e0",
            wraplength=320
        ).pack(anchor="w", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            details,
            text=file_path,
            font=("Segoe UI", 11),
            text_color="#64748b",
            wraplength=320
        ).pack(anchor="w", padx=16, pady=(0, 12))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=30, pady=(12, 20))

        ctk.CTkButton(
            btn_row,
            text="Open Folder",
            height=40,
            width=130,
            corner_radius=10,
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            font=("Segoe UI", 13, "bold"),
            command=self.open_folder
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_row,
            text="Close",
            height=40,
            width=130,
            corner_radius=10,
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=self.destroy
        ).pack(side="right", padx=(8, 0))

    def open_folder(self):
        import os
        folder = os.path.dirname(self.file_path)
        open_folder(folder)
