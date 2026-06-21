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
    "background": "#08090c",       # Obsidian
    "card": "#11131c",             # Dark slate card
    "card_light": "#181b29",       # Slightly lighter slate card
    "card_hover": "#1d2133",       # Hover state
    "text": "#f1f5f9",             # Slate-white text
    "muted": "#64748b",            # Muted text
    "primary": "#8b5cf6",          # Vibrant Violet
    "primary_hover": "#7c3aed",    # Darker Violet
    "accent": "#d946ef",           # Fuchsia/Magenta accent
    "success": "#10b981",          # Emerald green
    "danger": "#ef4444",           # Vibrant red
    "warning": "#f59e0b",          # Amber yellow
    "sidebar_bg": "#0d0e15",       # Darker sidebar
    "sidebar_hover": "#161924",    # Sidebar item hover
    "border": "#1e2235",           # Premium border color
    "glow_cyan": "#06b6d4",        # Cyan glow
    "glow_magenta": "#d946ef",     # Fuchsia glow
}


def get_theme(mode="modern"):
    if mode == "classic":
        return CLASSIC_THEME
    return MODERN_THEME
