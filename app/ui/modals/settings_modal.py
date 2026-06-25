import customtkinter as ctk
import tkinter.filedialog as filedialog


BROWSER_DISPLAY = ["None", "Chrome", "Firefox", "Edge", "Brave", "Opera", "Vivaldi"]
BROWSER_VALUE = {"None": "", "Chrome": "chrome", "Firefox": "firefox", "Edge": "edge", "Brave": "brave", "Opera": "opera", "Vivaldi": "vivaldi"}
DISPLAY_BROWSER = {v: k for k, v in BROWSER_VALUE.items()}


class SettingsModal(ctk.CTkToplevel):
    def __init__(self, parent, config, on_save):
        super().__init__(parent)

        self.title("Settings")
        self.geometry("520x620")
        self.resizable(False, False)

        self.config_data = config
        self.on_save = on_save

        self.transient(parent)
        self.grab_set()

        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text="Settings",
            font=("Segoe UI", 22, "bold"),
            text_color="#e0e0e0"
        ).pack(pady=(22, 16))

        notebook = ctk.CTkScrollableFrame(
            self,
            corner_radius=12,
            fg_color="transparent",
            height=420
        )
        notebook.pack(fill="x", padx=24, pady=(0, 12))

        categories = [
            ("General", [
                ("Theme", ["Dark", "Light", "System"], self.config_data.get("theme", "dark").capitalize(), "theme"),
                ("Auto Detect Platform", None, None, "auto_detect_platform"),
                ("Check for Updates on Startup", None, None, "check_updates_on_startup"),
                ("Show Completion Dialog", None, None, "show_completion_dialog"),
                ("Start with Windows", None, None, "start_with_windows"),
            ]),
            ("Downloads", [
                ("Default Quality", ["Best", "1080p", "720p", "480p", "MP3"], self.config_data.get("default_quality", "best").capitalize(), "default_quality"),
                ("Default File Type", ["Video", "Audio"], "Video", "default_file_type"),
                ("Filename Mode", ["Original", "Hash", "Mixed"], self.config_data.get("filename_mode", "original").capitalize(), "filename_mode"),
                ("Default Save To", None, None, "download_dir"),
            ]),
            ("Advanced", [
                ("Max Threads", ["1", "2", "3", "4", "5"], str(self.config_data.get("max_threads", 2)), "max_threads"),
                ("Save History", None, None, "save_history"),
            ]),
            ("Authentication", [
                ("Cookies File", None, None, "cookies_file"),
                ("Cookies From Browser", BROWSER_DISPLAY, self._get_browser_display(), "cookies_from_browser"),
            ]),
        ]

        self.menus = {}
        self.switches = {}
        self.entries = {}

        for cat_name, fields in categories:
            cat_frame = ctk.CTkFrame(notebook, corner_radius=12, fg_color="#1e2a45")
            cat_frame.pack(fill="x", pady=(0, 12))

            ctk.CTkLabel(
                cat_frame,
                text=cat_name,
                font=("Segoe UI", 14, "bold"),
                text_color="#8b5cf6"
            ).pack(anchor="w", padx=16, pady=(10, 4))

            for field in fields:
                label, values, default, key = field

                row = ctk.CTkFrame(cat_frame, fg_color="transparent")
                row.pack(fill="x", padx=16, pady=4)

                ctk.CTkLabel(
                    row,
                    text=label,
                    font=("Segoe UI", 13),
                    text_color="#c0c0c0",
                    width=180,
                    anchor="w"
                ).pack(side="left")

                if values:
                    menu = ctk.CTkOptionMenu(
                        row,
                        values=values,
                        width=180,
                        height=34,
                        corner_radius=8,
                        fg_color="#2a3a55",
                        button_color="#8b5cf6",
                        button_hover_color="#7c3aed",
                        dropdown_fg_color="#1e2a45",
                        dropdown_hover_color="#2a3a55",
                        text_color="#e0e0e0",
                        dropdown_text_color="#e0e0e0",
                        font=("Segoe UI", 13),
                        dropdown_font=("Segoe UI", 13)
                    )
                    menu.pack(side="right")
                    if default:
                        menu.set(default)
                    self.menus[key] = menu

                elif key == "download_dir":
                    entry = ctk.CTkEntry(
                        row,
                        width=180,
                        height=34,
                        corner_radius=8,
                        fg_color="#2a3a55",
                        border_width=1,
                        border_color="#2a3a55",
                        text_color="#e0e0e0"
                    )
                    entry.pack(side="right")
                    entry.insert(0, self.config_data.get("download_dir"))
                    self.entries[key] = entry

                elif key == "cookies_file":
                    frame = ctk.CTkFrame(row, fg_color="transparent")
                    frame.pack(side="right")
                    entry = ctk.CTkEntry(
                        frame,
                        width=130,
                        height=34,
                        corner_radius=8,
                        fg_color="#2a3a55",
                        border_width=1,
                        border_color="#2a3a55",
                        text_color="#e0e0e0"
                    )
                    entry.pack(side="left")
                    entry.insert(0, self.config_data.get("cookies_file", ""))
                    self.entries[key] = entry
                    ctk.CTkButton(
                        frame,
                        text="Browse",
                        width=50,
                        height=34,
                        corner_radius=8,
                        fg_color="#8b5cf6",
                        hover_color="#7c3aed",
                        font=("Segoe UI", 12),
                        command=lambda e=entry: self._browse_cookies(e)
                    ).pack(side="left", padx=(4, 0))

                else:
                    val = self.config_data.get(key, True)
                    switch = ctk.CTkSwitch(
                        row,
                        text="",
                        width=40,
                        fg_color="#2a3a55",
                        progress_color="#8b5cf6",
                        button_color="#64748b",
                        button_hover_color="#8b5cf6"
                    )
                    switch.pack(side="right")
                    switch.select() if val else switch.deselect()
                    self.switches[key] = switch

        ctk.CTkButton(
            self,
            text="Save Settings",
            height=42,
            corner_radius=12,
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            font=("Segoe UI", 14, "bold"),
            command=self.save
        ).pack(fill="x", padx=30, pady=(8, 6))

        ctk.CTkButton(
            self,
            text="Cancel",
            height=42,
            corner_radius=12,
            fg_color="#6b7280",
            hover_color="#4b5563",
            font=("Segoe UI", 14),
            command=self.destroy
        ).pack(fill="x", padx=30, pady=6)

    def _get_browser_display(self):
        val = self.config_data.get("cookies_from_browser", "")
        return DISPLAY_BROWSER.get(val, "None")

    def _browse_cookies(self, entry):
        path = filedialog.askopenfilename(
            title="Select cookies.txt file",
            filetypes=[("Text files", "*.txt"), ("Netscape cookies", "*"), ("All files", "*.*")]
        )
        if path:
            entry.delete(0, "end")
            entry.insert(0, path)

    def save(self):
        def to_key(val):
            mapping = {
                "dark": "dark", "light": "light", "system": "system",
                "best": "best", "1080p": "1080p", "720p": "720p", "480p": "480p", "mp3": "mp3",
                "original": "original", "hash": "hash", "mixed": "mixed",
                "video": "video", "audio": "audio",
            }
            if val in mapping:
                return mapping[val]
            return val.lower().replace(" ", "_")

        new_config = {}

        for key, menu in self.menus.items():
            val = menu.get()
            if key == "cookies_from_browser":
                new_config[key] = BROWSER_VALUE.get(val, "")
            elif key in ("theme", "default_quality", "filename_mode", "max_threads"):
                new_config[key] = to_key(val)
            else:
                new_config[key] = to_key(val)

        if "download_dir" in self.entries:
            new_config["download_dir"] = self.entries["download_dir"].get().strip()

        if "cookies_file" in self.entries:
            new_config["cookies_file"] = self.entries["cookies_file"].get().strip()

        for key, switch in self.switches.items():
            new_config[key] = bool(switch.get())

        self.on_save(new_config)
        self.destroy()
