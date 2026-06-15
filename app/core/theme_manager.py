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
    "background": "#0b0e1a",
    "card": "#13172b",
    "card_light": "#1c2140",
    "card_hover": "#252b50",
    "text": "#f1f5f9",
    "muted": "#64748b",
    "primary": "#8b5cf6",
    "primary_hover": "#7c3aed",
    "success": "#22c55e",
    "danger": "#ef4444",
    "warning": "#f59e0b",
    "sidebar_bg": "#090c17",
    "sidebar_hover": "#1a1f3a",
    "border": "#1e2448",
    "glow": "rgba(139, 92, 246, 0.15)",
}


def get_theme(mode="modern"):
    if mode == "classic":
        return CLASSIC_THEME
    return MODERN_THEME
