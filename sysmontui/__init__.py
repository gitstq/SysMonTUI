"""
SysMonTUI - Lightweight Cross-Platform System Monitor TUI

A beautiful terminal-based system resource monitor with real-time
CPU, Memory, Disk, and Network monitoring capabilities.

Author: gitstq
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"
__title__ = "SysMonTUI"
__description__ = "Lightweight Cross-Platform System Monitor TUI"

from sysmontui.app import SysMonApp

__all__ = ["SysMonApp", "__version__"]
