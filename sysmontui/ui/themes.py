"""Theme configuration for SysMonTUI."""
from typing import Dict


class Theme:
    """Color theme for the application."""

    def __init__(self):
        # Header colors
        self.header_bg = "blue"
        self.header_fg = "white"

        # Panel colors
        self.panel_border = "blue"
        self.panel_title = "cyan"

        # Metric colors
        self.metric_label = "cyan"
        self.metric_value = "white"
        self.metric_unit = "dim"

        # Status colors
        self.status_normal = "green"
        self.status_warning = "yellow"
        self.status_critical = "red"

        # Chart colors
        self.chart_line = "cyan"
        self.chart_fill = "blue"

        # Text colors
        self.text_normal = "white"
        self.text_dim = "dim"
        self.text_highlight = "bright_white"

        # Key binding colors
        self.key_binding = "yellow"
        self.key_description = "white"

    def get_status_color(self, percent: float) -> str:
        """Get color based on percentage."""
        if percent < 50:
            return self.status_normal
        elif percent < 80:
            return self.status_warning
        else:
            return self.status_critical


class DarkTheme(Theme):
    """Dark color theme."""

    def __init__(self):
        super().__init__()
        self.header_bg = "dark_blue"
        self.panel_border = "bright_black"


class LightTheme(Theme):
    """Light color theme."""

    def __init__(self):
        super().__init__()
        self.header_bg = "blue"
        self.header_fg = "white"
        self.panel_border = "blue"
        self.text_normal = "black"
        self.text_dim = "bright_black"


# Default theme
DEFAULT_THEME = Theme()
