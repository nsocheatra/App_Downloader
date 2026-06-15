CLASSIC_THEME = {
    "background": "#f5f5f5",
    "card": "#ffffff",
    "border": "#d1d5db",
    "text": "#111827",
    "muted": "#6b7280",
    "primary": "#3b82f6",
    "success": "#22c55e",
    "danger": "#ef4444",
}

MODERN_THEME = {
    "background": "#050505",       # Deep black/gray
    "card": "#111111",             # Slightly lighter black
    "card_light": "#1a1a1a",       # Lighter card element
    "card_hover": "#222222",       # Hover state
    "text": "#e0e0e0",             # Bright text
    "muted": "#888888",            # Muted text
    "primary": "#00f0ff",          # Neon cyan
    "primary_hover": "#00c3cc",    # Darker neon cyan
    "accent": "#ff003c",           # Neon pink/red accent
    "success": "#39ff14",          # Neon green
    "danger": "#ff003c",           # Cyberpunk red
    "warning": "#fcee0a",          # Cyberpunk yellow
    "sidebar_bg": "#080808",       # Deep sidebar
    "sidebar_hover": "#141414",    # Sidebar hover
    "border": "#2a2a2a",           # Dark border
    "glow_cyan": "#00f0ff",        # For hover glow
    "glow_magenta": "#ff00ff",     # For alternative hover glow
}


def get_theme(mode="modern"):
    if mode == "classic":
        return CLASSIC_THEME
    return MODERN_THEME
