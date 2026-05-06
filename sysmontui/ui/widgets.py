"""Custom UI widgets for SysMonTUI."""
from typing import List, Optional, Tuple
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.bar import Bar
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout

from sysmontui.utils.formatters import (
    format_bytes, format_bytes_per_sec, format_percent,
    get_color_for_percent, get_bar_char
)


def create_header(version: str = "1.0.0") -> Panel:
    """Create the application header."""
    title = Text("SysMonTUI", style="bold cyan")
    subtitle = Text(f" v{version}", style="dim")
    header_text = Text.assemble(title, subtitle)

    tabs = Text("[CPU] [MEM] [DISK] [NET] [PROC]", style="yellow")

    return Panel(
        header_text,
        title=tabs,
        title_align="right",
        border_style="blue",
        padding=(0, 1)
    )


def create_footer() -> Panel:
    """Create the application footer with key bindings."""
    keys = [
        ("q", "Quit"),
        ("1", "CPU"),
        ("2", "Memory"),
        ("3", "Disk"),
        ("4", "Network"),
        ("5", "Process"),
        ("↑/↓", "Scroll"),
        ("r", "Refresh"),
    ]

    text = Text()
    for i, (key, desc) in enumerate(keys):
        if i > 0:
            text.append("  ")
        text.append(f"[{key}]", style="yellow bold")
        text.append(f" {desc}", style="white")

    return Panel(text, border_style="blue", padding=(0, 1))


def create_metric_row(label: str, value: str, percent: Optional[float] = None,
                     unit: str = "", width: int = 30) -> Text:
    """Create a metric display row."""
    text = Text()
    text.append(f"{label:12}", style="cyan")

    if percent is not None:
        color = get_color_for_percent(percent)
        bar = get_bar_char(percent, width=20)
        text.append(f" {bar} ", style=color)
        text.append(f"{value:>8}", style="white bold")
    else:
        text.append(f"{value:>30}", style="white bold")

    if unit:
        text.append(f" {unit}", style="dim")

    return text


def create_cpu_panel(cpu_info, history: Optional[List[float]] = None) -> Panel:
    """Create CPU information panel."""
    from sysmontui.utils.formatters import format_hz

    content = Text()

    # Overall CPU usage
    percent = cpu_info.percent
    color = get_color_for_percent(percent)
    bar = get_bar_char(percent, width=25)

    content.append("Total Usage:\n", style="cyan")
    content.append(f"  {bar} ", style=color)
    content.append(f"{percent:.1f}%\n\n", style="white bold")

    # Per-core usage
    content.append("Per Core:\n", style="cyan")
    cores = cpu_info.percent_per_cpu
    for i in range(0, len(cores), 4):
        line_cores = cores[i:i+4]
        for j, p in enumerate(line_cores):
            core_num = i + j
            color = get_color_for_percent(p)
            content.append(f"  C{core_num:2d}:", style="dim")
            content.append(f"{p:5.1f}%", style=color)
        content.append("\n")

    # Frequency info
    if cpu_info.freq_current:
        content.append(f"\nFrequency: ", style="cyan")
        content.append(f"{format_hz(cpu_info.freq_current * 1e6)}", style="white")
        if cpu_info.freq_min and cpu_info.freq_max:
            content.append(f" (min: {format_hz(cpu_info.freq_min * 1e6)}, max: {format_hz(cpu_info.freq_max * 1e6)})", style="dim")

    # CPU info
    content.append(f"\nCores: ", style="cyan")
    content.append(f"{cpu_info.core_count} physical, {cpu_info.thread_count} logical", style="white")

    return Panel(content, title="[CPU] Processor", border_style="blue", padding=(1, 2))


def create_memory_panel(mem_info) -> Panel:
    """Create memory information panel."""
    content = Text()

    # Memory usage bar
    percent = mem_info.percent
    color = get_color_for_percent(percent)
    bar = get_bar_char(percent, width=30)

    content.append("Memory Usage:\n", style="cyan")
    content.append(f"  {bar} ", style=color)
    content.append(f"{percent:.1f}%\n", style="white bold")
    content.append(f"  {format_bytes(mem_info.used)} / {format_bytes(mem_info.total)} used\n", style="dim")
    content.append(f"  {format_bytes(mem_info.available)} available\n\n", style="dim")

    # Swap memory
    if mem_info.swap_total > 0:
        swap_percent = mem_info.swap_percent
        swap_color = get_color_for_percent(swap_percent)
        swap_bar = get_bar_char(swap_percent, width=30)

        content.append("Swap Usage:\n", style="cyan")
        content.append(f"  {swap_bar} ", style=swap_color)
        content.append(f"{swap_percent:.1f}%\n", style="white bold")
        content.append(f"  {format_bytes(mem_info.swap_used)} / {format_bytes(mem_info.swap_total)} used\n", style="dim")

    return Panel(content, title="[MEM] Memory", border_style="blue", padding=(1, 2))


def create_disk_panel(partitions) -> Panel:
    """Create disk information panel."""
    table = Table(show_header=True, header_style="bold cyan", box=None)
    table.add_column("Device", style="cyan", width=12)
    table.add_column("Mount", style="white", width=15)
    table.add_column("Type", style="dim", width=8)
    table.add_column("Usage", style="white", width=20)
    table.add_column("Size", style="dim", width=12)

    for part in partitions[:6]:  # Limit to 6 partitions
        percent = part.percent
        color = get_color_for_percent(percent)
        bar = get_bar_char(percent, width=15)

        usage_text = Text()
        usage_text.append(f"{bar} ", style=color)
        usage_text.append(f"{percent:.0f}%", style="white")

        table.add_row(
            part.device.split('/')[-1][:12],
            part.mountpoint[:15],
            part.fstype[:8] if part.fstype else "-",
            usage_text,
            format_bytes(part.total)
        )

    return Panel(table, title="[DISK] Storage", border_style="blue", padding=(1, 1))


def create_network_panel(interfaces) -> Panel:
    """Create network information panel."""
    table = Table(show_header=True, header_style="bold cyan", box=None)
    table.add_column("Interface", style="cyan", width=12)
    table.add_column("Status", style="white", width=8)
    table.add_column("Download", style="green", width=12)
    table.add_column("Upload", style="blue", width=12)
    table.add_column("Packets", style="dim", width=15)

    for iface in interfaces[:6]:  # Limit to 6 interfaces
        status = "UP" if iface.is_up else "DOWN"
        status_style = "green" if iface.is_up else "red"

        table.add_row(
            iface.name[:12],
            Text(status, style=status_style),
            format_bytes(iface.bytes_recv),
            format_bytes(iface.bytes_sent),
            f"↓{iface.packets_recv}/↑{iface.packets_sent}"
        )

    return Panel(table, title="[NET] Network", border_style="blue", padding=(1, 1))


def create_process_panel(processes) -> Panel:
    """Create process list panel."""
    table = Table(show_header=True, header_style="bold cyan", box=None)
    table.add_column("PID", style="cyan", width=8, justify="right")
    table.add_column("Name", style="white", width=20)
    table.add_column("CPU%", style="yellow", width=8, justify="right")
    table.add_column("MEM%", style="green", width=8, justify="right")
    table.add_column("Memory", style="dim", width=12, justify="right")
    table.add_column("Status", style="dim", width=10)

    for proc in processes[:15]:  # Limit to 15 processes
        cpu_color = get_color_for_percent(proc.cpu_percent)
        mem_color = get_color_for_percent(proc.memory_percent)

        table.add_row(
            str(proc.pid),
            proc.name[:20],
            Text(f"{proc.cpu_percent:.1f}", style=cpu_color),
            Text(f"{proc.memory_percent:.1f}", style=mem_color),
            format_bytes(proc.memory_rss),
            proc.status[:10]
        )

    return Panel(table, title="[PROC] Top Processes", border_style="blue", padding=(1, 1))
