"""Main dashboard UI for SysMonTUI."""
import sys
from typing import Optional, List
from datetime import datetime

from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from sysmontui.monitors import CPUMonitor, MemoryMonitor, DiskMonitor, NetworkMonitor, ProcessMonitor
from sysmontui.utils.history import HistoryManager
from sysmontui.ui.widgets import (
    create_header, create_footer, create_cpu_panel,
    create_memory_panel, create_disk_panel, create_network_panel,
    create_process_panel
)


class Dashboard:
    """Main dashboard controller."""

    VIEWS = ["overview", "cpu", "memory", "disk", "network", "process"]

    def __init__(self, refresh_rate: float = 1.0, history_size: int = 60):
        self.console = Console()
        self.refresh_rate = refresh_rate
        self.history_size = history_size

        # Monitors
        self.cpu_monitor = CPUMonitor()
        self.memory_monitor = MemoryMonitor()
        self.disk_monitor = DiskMonitor()
        self.network_monitor = NetworkMonitor()
        self.process_monitor = ProcessMonitor()

        # History
        self.history = HistoryManager(buffer_size=history_size)

        # State
        self.current_view = "overview"
        self.running = False
        self.show_help = False

    def update_data(self) -> None:
        """Update all monitoring data."""
        # CPU
        cpu_info = self.cpu_monitor.get_info()
        self.history.record("cpu_percent", cpu_info.percent)
        for i, p in enumerate(cpu_info.percent_per_cpu):
            self.history.record(f"cpu_core_{i}", p)

        # Memory
        mem_info = self.memory_monitor.get_info()
        self.history.record("memory_percent", mem_info.percent)
        self.history.record("swap_percent", mem_info.swap_percent)

    def create_overview_layout(self) -> Layout:
        """Create the overview layout."""
        layout = Layout()

        # Header
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )

        # Main content split
        layout["main"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )

        # Left column
        layout["left"].split_column(
            Layout(name="cpu"),
            Layout(name="memory")
        )

        # Right column
        layout["right"].split_column(
            Layout(name="disk"),
            Layout(name="network")
        )

        # Update content
        self.update_data()

        cpu_info = self.cpu_monitor.get_info()
        mem_info = self.memory_monitor.get_info()
        disk_partitions = self.disk_monitor.get_partitions()
        network_interfaces = self.network_monitor.get_interfaces()

        layout["header"].update(create_header())
        layout["cpu"].update(create_cpu_panel(cpu_info, self.history.get_values("cpu_percent")))
        layout["memory"].update(create_memory_panel(mem_info))
        layout["disk"].update(create_disk_panel(disk_partitions))
        layout["network"].update(create_network_panel(network_interfaces))
        layout["footer"].update(create_footer())

        return layout

    def create_cpu_view(self) -> Panel:
        """Create CPU detailed view."""
        cpu_info = self.cpu_monitor.get_info()
        history = self.history.get_values("cpu_percent")

        content = Text()

        # CPU brand
        brand = self.cpu_monitor.get_cpu_brand()
        content.append(f"CPU: {brand}\n\n", style="bold cyan")

        # Overall usage with large bar
        percent = cpu_info.percent
        color = "green" if percent < 50 else "yellow" if percent < 80 else "red"

        from sysmontui.utils.formatters import get_bar_char
        bar = get_bar_char(percent, width=50)

        content.append("Overall Usage:\n", style="cyan")
        content.append(f"{bar}\n", style=color)
        content.append(f"{percent:.1f}%\n\n", style="white bold")

        # Per-core detailed view
        content.append("Per-Core Usage:\n", style="cyan")
        cores = cpu_info.percent_per_cpu

        for i, p in enumerate(cores):
            core_color = "green" if p < 50 else "yellow" if p < 80 else "red"
            core_bar = get_bar_char(p, width=40)
            content.append(f"  Core {i:2d}: {core_bar} {p:5.1f}%\n", style=core_color)

        # CPU times
        content.append("\nCPU Times:\n", style="cyan")
        times = self.cpu_monitor.get_cpu_times()
        for key, value in times.items():
            content.append(f"  {key:12}: {value:.2f}s\n", style="white")

        # Load average (Unix only)
        load_avg = self.cpu_monitor.get_load_average()
        if load_avg:
            content.append(f"\nLoad Average:\n", style="cyan")
            content.append(f"  1min: {load_avg[0]:.2f}, 5min: {load_avg[1]:.2f}, 15min: {load_avg[2]:.2f}\n", style="white")

        # Frequency
        if cpu_info.freq_current:
            from sysmontui.utils.formatters import format_hz
            content.append(f"\nFrequency: ", style="cyan")
            content.append(f"{format_hz(cpu_info.freq_current * 1e6)}\n", style="white")

        return Panel(content, title="[CPU] Detailed View", border_style="blue", padding=(1, 2))

    def create_memory_view(self) -> Panel:
        """Create memory detailed view."""
        mem_info = self.memory_monitor.get_info()

        content = Text()

        # Virtual Memory
        content.append("Virtual Memory:\n", style="bold cyan")
        percent = mem_info.percent
        color = "green" if percent < 50 else "yellow" if percent < 80 else "red"
        from sysmontui.utils.formatters import get_bar_char
        bar = get_bar_char(percent, width=50)

        content.append(f"{bar}\n", style=color)
        content.append(f"Usage: {percent:.1f}%\n\n", style="white bold")

        # Memory details table
        table = Table(show_header=False, box=None)
        table.add_column("Label", style="cyan", width=15)
        table.add_column("Value", style="white", width=15)

        table.add_row("Total", f"{mem_info.total / (1024**3):.2f} GB")
        table.add_row("Used", f"{mem_info.used / (1024**3):.2f} GB")
        table.add_row("Available", f"{mem_info.available / (1024**3):.2f} GB")
        table.add_row("Free", f"{mem_info.free / (1024**3):.2f} GB")

        if mem_info.cached:
            table.add_row("Cached", f"{mem_info.cached / (1024**3):.2f} GB")
        if mem_info.buffers:
            table.add_row("Buffers", f"{mem_info.buffers / (1024**3):.2f} GB")
        if mem_info.shared:
            table.add_row("Shared", f"{mem_info.shared / (1024**3):.2f} GB")

        # Render table as string
        from rich import box
        table.box = box.SIMPLE
        with self.console.capture() as capture:
            self.console.print(table)
        content.append(capture.get())

        # Swap Memory
        if mem_info.swap_total > 0:
            content.append("\n\nSwap Memory:\n", style="bold cyan")
            swap_percent = mem_info.swap_percent
            swap_color = "green" if swap_percent < 50 else "yellow" if swap_percent < 80 else "red"
            swap_bar = get_bar_char(swap_percent, width=50)

            content.append(f"{swap_bar}\n", style=swap_color)
            content.append(f"Usage: {swap_percent:.1f}%\n", style="white bold")

            swap_table = Table(show_header=False, box=None)
            swap_table.add_column("Label", style="cyan", width=15)
            swap_table.add_column("Value", style="white", width=15)

            swap_table.add_row("Total", f"{mem_info.swap_total / (1024**3):.2f} GB")
            swap_table.add_row("Used", f"{mem_info.swap_used / (1024**3):.2f} GB")
            swap_table.add_row("Free", f"{mem_info.swap_free / (1024**3):.2f} GB")

            swap_table.box = box.SIMPLE
            with self.console.capture() as capture:
                self.console.print(swap_table)
            content.append(capture.get())

        return Panel(content, title="[MEM] Detailed View", border_style="blue", padding=(1, 2))

    def create_disk_view(self) -> Panel:
        """Create disk detailed view."""
        partitions = self.disk_monitor.get_partitions()

        content = Text()

        # Partitions table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Device", style="cyan", width=12)
        table.add_column("Mount", style="white", width=20)
        table.add_column("Type", style="dim", width=8)
        table.add_column("Total", style="white", width=12, justify="right")
        table.add_column("Used", style="yellow", width=12, justify="right")
        table.add_column("Free", style="green", width=12, justify="right")
        table.add_column("Usage", style="white", width=15)

        for part in partitions:
            from sysmontui.utils.formatters import get_bar_char, get_color_for_percent
            percent = part.percent
            color = get_color_for_percent(percent)
            bar = get_bar_char(percent, width=10)

            usage_text = Text()
            usage_text.append(f"{bar} ", style=color)
            usage_text.append(f"{percent:.0f}%", style="white")

            table.add_row(
                part.device.split('/')[-1][:12],
                part.mountpoint[:20],
                part.fstype[:8] if part.fstype else "-",
                f"{part.total / (1024**3):.1f}G",
                f"{part.used / (1024**3):.1f}G",
                f"{part.free / (1024**3):.1f}G",
                usage_text
            )

        with self.console.capture() as capture:
            self.console.print(table)
        content.append(capture.get())

        # I/O counters
        io_counters = self.disk_monitor.get_io_counters()
        if io_counters and "total" in io_counters:
            io = io_counters["total"]
            content.append("\n\nDisk I/O Statistics:\n", style="bold cyan")
            content.append(f"  Read:  {io.read_bytes / (1024**3):.2f} GB ({io.read_count} ops)\n", style="white")
            content.append(f"  Write: {io.write_bytes / (1024**3):.2f} GB ({io.write_count} ops)\n", style="white")

        return Panel(content, title="[DISK] Detailed View", border_style="blue", padding=(1, 2))

    def create_network_view(self) -> Panel:
        """Create network detailed view."""
        interfaces = self.network_monitor.get_interfaces()
        connections = self.network_monitor.get_connections()

        content = Text()

        # Interfaces table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Interface", style="cyan", width=12)
        table.add_column("Status", style="white", width=8)
        table.add_column("Speed", style="dim", width=10)
        table.add_column("MTU", style="dim", width=8)
        table.add_column("Download", style="green", width=12)
        table.add_column("Upload", style="blue", width=12)
        table.add_column("Packets In/Out", style="dim", width=18)

        for iface in interfaces:
            status = "UP" if iface.is_up else "DOWN"
            status_style = "green" if iface.is_up else "red"

            speed = f"{iface.speed} Mbps" if iface.speed else "Unknown"

            table.add_row(
                iface.name[:12],
                Text(status, style=status_style),
                speed,
                str(iface.mtu),
                f"{iface.bytes_recv / (1024**2):.1f} MB",
                f"{iface.bytes_sent / (1024**2):.1f} MB",
                f"{iface.packets_recv} / {iface.packets_sent}"
            )

        with self.console.capture() as capture:
            self.console.print(table)
        content.append(capture.get())

        # Connection count
        content.append(f"\n\nActive Connections: {len(connections)}\n", style="bold cyan")

        # Connection status breakdown
        status_counts = {}
        for conn in connections:
            status_counts[conn.status] = status_counts.get(conn.status, 0) + 1

        if status_counts:
            content.append("Connection Status:\n", style="cyan")
            for status, count in sorted(status_counts.items()):
                content.append(f"  {status}: {count}\n", style="white")

        return Panel(content, title="[NET] Detailed View", border_style="blue", padding=(1, 2))

    def create_process_view(self) -> Panel:
        """Create process detailed view."""
        processes = self.process_monitor.get_processes(sort_by="cpu", limit=20)
        process_count = self.process_monitor.get_process_count()
        status_counts = self.process_monitor.get_process_count_by_status()

        content = Text()

        # Process statistics
        content.append(f"Total Processes: {process_count}\n", style="bold cyan")
        content.append("Status: ", style="cyan")
        for status, count in sorted(status_counts.items()):
            content.append(f"{status}={count} ", style="white")
        content.append("\n\n")

        # Process table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("PID", style="cyan", width=8, justify="right")
        table.add_column("Name", style="white", width=20)
        table.add_column("User", style="dim", width=12)
        table.add_column("CPU%", style="yellow", width=8, justify="right")
        table.add_column("MEM%", style="green", width=8, justify="right")
        table.add_column("RSS", style="white", width=10, justify="right")
        table.add_column("VMS", style="dim", width=10, justify="right")
        table.add_column("Threads", style="dim", width=8, justify="right")
        table.add_column("Status", style="dim", width=10)

        for proc in processes:
            cpu_color = "green" if proc.cpu_percent < 50 else "yellow" if proc.cpu_percent < 80 else "red"
            mem_color = "green" if proc.memory_percent < 50 else "yellow" if proc.memory_percent < 80 else "red"

            table.add_row(
                str(proc.pid),
                proc.name[:20],
                (proc.username or "-")[:12],
                Text(f"{proc.cpu_percent:.1f}", style=cpu_color),
                Text(f"{proc.memory_percent:.1f}", style=mem_color),
                f"{proc.memory_rss / (1024**2):.1f}M",
                f"{proc.memory_vms / (1024**2):.1f}M",
                str(proc.num_threads),
                proc.status[:10]
            )

        with self.console.capture() as capture:
            self.console.print(table)
        content.append(capture.get())

        return Panel(content, title="[PROC] Process View", border_style="blue", padding=(1, 2))

    def render(self) -> Layout:
        """Render the current view."""
        if self.current_view == "overview":
            return self.create_overview_layout()

        # Create layout with header, main, footer
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )

        layout["header"].update(create_header())
        layout["footer"].update(create_footer())

        if self.current_view == "cpu":
            layout["main"].update(self.create_cpu_view())
        elif self.current_view == "memory":
            layout["main"].update(self.create_memory_view())
        elif self.current_view == "disk":
            layout["main"].update(self.create_disk_view())
        elif self.current_view == "network":
            layout["main"].update(self.create_network_view())
        elif self.current_view == "process":
            layout["main"].update(self.create_process_view())

        return layout

    def handle_input(self, key: str) -> bool:
        """Handle keyboard input. Returns False if should exit."""
        if key == "q" or key == "Q":
            return False
        elif key == "1":
            self.current_view = "cpu"
        elif key == "2":
            self.current_view = "memory"
        elif key == "3":
            self.current_view = "disk"
        elif key == "4":
            self.current_view = "network"
        elif key == "5":
            self.current_view = "process"
        elif key == "0":
            self.current_view = "overview"
        elif key == "h" or key == "?":
            self.show_help = not self.show_help

        return True
