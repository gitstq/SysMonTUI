"""Main application module for SysMonTUI."""
import sys
import time
import signal
import threading
from typing import Optional

try:
    import termios
    import tty
    import select
    TERMINAL_AVAILABLE = True
except ImportError:
    TERMINAL_AVAILABLE = False

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from sysmontui.ui.dashboard import Dashboard


class SysMonApp:
    """Main SysMonTUI application."""

    def __init__(self, refresh_rate: float = 1.0):
        self.console = Console()
        self.refresh_rate = refresh_rate
        self.dashboard = Dashboard(refresh_rate=refresh_rate)
        self.running = False
        self._input_thread: Optional[threading.Thread] = None
        self._last_key: Optional[str] = None

    def _read_key(self) -> Optional[str]:
        """Read a single keypress from stdin."""
        if not TERMINAL_AVAILABLE:
            return None

        try:
            # Check if input is available
            if select.select([sys.stdin], [], [], 0)[0]:
                return sys.stdin.read(1)
        except:
            pass
        return None

    def _input_loop(self) -> None:
        """Background thread for reading input."""
        if not TERMINAL_AVAILABLE:
            return

        # Save terminal settings
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            # Set terminal to raw mode
            tty.setcbreak(sys.stdin.fileno())

            while self.running:
                key = self._read_key()
                if key:
                    self._last_key = key
                time.sleep(0.05)
        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    def _handle_signals(self) -> None:
        """Setup signal handlers."""
        def signal_handler(signum, frame):
            self.running = False

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def run(self) -> None:
        """Run the application."""
        self._handle_signals()
        self.running = True

        # Start input thread if terminal is available
        if TERMINAL_AVAILABLE:
            self._input_thread = threading.Thread(target=self._input_loop, daemon=True)
            self._input_thread.start()

        try:
            with Live(
                self.dashboard.render(),
                console=self.console,
                refresh_per_second=1 / self.refresh_rate,
                screen=True,
                transient=False
            ) as live:
                while self.running:
                    # Handle input
                    if self._last_key:
                        key = self._last_key
                        self._last_key = None
                        if not self.dashboard.handle_input(key):
                            self.running = False
                            break

                    # Update dashboard data
                    self.dashboard.update_data()

                    # Update display
                    live.update(self.dashboard.render())

                    # Small sleep to prevent high CPU usage
                    time.sleep(self.refresh_rate)

        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            self.console.clear()
            self.console.print("[cyan]SysMonTUI[/cyan] stopped. Goodbye! 👋")

    def run_simple(self) -> None:
        """Run in simple mode without live updates (for testing)."""
        self.dashboard.update_data()
        layout = self.dashboard.render()
        self.console.print(layout)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="SysMonTUI - Lightweight Cross-Platform System Monitor TUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Keyboard Shortcuts:
  0         Overview mode (all panels)
  1         CPU detailed view
  2         Memory detailed view
  3         Disk detailed view
  4         Network detailed view
  5         Process detailed view
  q         Quit
  h, ?      Toggle help

Examples:
  sysmontui              # Run with default 1 second refresh
  sysmontui -r 0.5       # Run with 0.5 second refresh
  sysmontui --once       # Display once and exit
        """
    )

    parser.add_argument(
        "-r", "--refresh",
        type=float,
        default=1.0,
        metavar="RATE",
        help="Refresh rate in seconds (default: 1.0)"
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help="Display system info once and exit"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    args = parser.parse_args()

    app = SysMonApp(refresh_rate=args.refresh)

    if args.once:
        app.run_simple()
    else:
        app.run()


if __name__ == "__main__":
    main()
