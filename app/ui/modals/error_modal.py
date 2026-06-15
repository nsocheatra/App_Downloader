import customtkinter as ctk


class ErrorModal(ctk.CTkToplevel):
    def __init__(self, parent, title, reason, suggestion=None):
        super().__init__(parent)

        self.title(title)
        self.geometry("420x280")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.build_ui(title, reason, suggestion)

    def build_ui(self, title, reason, suggestion):
        ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 20, "bold"),
            text_color="#ef4444"
        ).pack(pady=(24, 16))

        content = ctk.CTkFrame(self, corner_radius=12, fg_color="#1e2a45")
        content.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(
            content,
            text="Reason:",
            font=("Segoe UI", 12, "bold"),
            text_color="#8899aa"
        ).pack(anchor="w", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            content,
            text=reason,
            font=("Segoe UI", 13),
            text_color="#e0e0e0",
            wraplength=340,
            justify="left"
        ).pack(anchor="w", padx=16, pady=(0, 8))

        if suggestion:
            ctk.CTkLabel(
                content,
                text="Suggestion:",
                font=("Segoe UI", 12, "bold"),
                text_color="#8899aa"
            ).pack(anchor="w", padx=16, pady=(4, 4))

            ctk.CTkLabel(
                content,
                text=suggestion,
                font=("Segoe UI", 13),
                text_color="#fbbf24",
                wraplength=340,
                justify="left"
            ).pack(anchor="w", padx=16, pady=(0, 12))

        ctk.CTkButton(
            self,
            text="OK",
            height=40,
            corner_radius=12,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=("Segoe UI", 14, "bold"),
            command=self.destroy
        ).pack(pady=(10, 20))
