"""Data formatting utilities."""


def format_bytes(bytes_value: int, precision: int = 2) -> str:
    """Format bytes to human readable string."""
    if bytes_value < 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    unit_index = 0
    value = float(bytes_value)

    while value >= 1024.0 and unit_index < len(units) - 1:
        value /= 1024.0
        unit_index += 1

    return f"{value:.{precision}f} {units[unit_index]}"


def format_bytes_per_sec(bytes_value: int, precision: int = 2) -> str:
    """Format bytes per second to human readable string."""
    return f"{format_bytes(bytes_value, precision)}/s"


def format_hz(hz_value: float, precision: int = 2) -> str:
    """Format Hz to human readable string."""
    if hz_value < 1000:
        return f"{hz_value:.{precision}f} Hz"
    elif hz_value < 1000000:
        return f"{hz_value / 1000:.{precision}f} MHz"
    else:
        return f"{hz_value / 1000000:.{precision}f} GHz"


def format_percent(value: float, precision: int = 1) -> str:
    """Format percentage value."""
    return f"{value:.{precision}f}%"


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human readable string."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        return f"{days}d {hours}h"


def format_number(num: int) -> str:
    """Format large numbers with K/M/B suffix."""
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return f"{num / 1000:.1f}K"
    elif num < 1000000000:
        return f"{num / 1000000:.1f}M"
    else:
        return f"{num / 1000000000:.1f}B"


def get_color_for_percent(percent: float) -> str:
    """Get color based on percentage value."""
    if percent < 50:
        return "green"
    elif percent < 80:
        return "yellow"
    else:
        return "red"


def get_bar_char(percent: float, width: int = 20) -> str:
    """Generate a progress bar character string."""
    filled = int(width * percent / 100)
    empty = width - filled
    return "█" * filled + "░" * empty
