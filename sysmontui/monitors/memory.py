"""Memory monitoring module."""
import psutil
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class MemoryInfo:
    """Memory information data class."""
    # Virtual memory
    total: int
    available: int
    percent: float
    used: int
    free: int
    active: Optional[int]
    inactive: Optional[int]
    buffers: Optional[int]
    cached: Optional[int]
    shared: Optional[int]

    # Swap memory
    swap_total: int
    swap_used: int
    swap_free: int
    swap_percent: float
    swap_sin: int
    swap_sout: int


class MemoryMonitor:
    """Monitor memory usage and information."""

    def get_info(self) -> MemoryInfo:
        """Get comprehensive memory information."""
        # Virtual memory
        vm = psutil.virtual_memory()

        # Swap memory
        sm = psutil.swap_memory()

        return MemoryInfo(
            total=vm.total,
            available=vm.available,
            percent=vm.percent,
            used=vm.used,
            free=vm.free,
            active=getattr(vm, 'active', None),
            inactive=getattr(vm, 'inactive', None),
            buffers=getattr(vm, 'buffers', None),
            cached=getattr(vm, 'cached', None),
            shared=getattr(vm, 'shared', None),
            swap_total=sm.total,
            swap_used=sm.used,
            swap_free=sm.free,
            swap_percent=sm.percent,
            swap_sin=sm.sin,
            swap_sout=sm.sout,
        )

    def get_virtual_memory(self) -> Dict[str, any]:
        """Get virtual memory information."""
        vm = psutil.virtual_memory()
        return {
            "total": vm.total,
            "available": vm.available,
            "percent": vm.percent,
            "used": vm.used,
            "free": vm.free,
            "active": getattr(vm, 'active', None),
            "inactive": getattr(vm, 'inactive', None),
            "buffers": getattr(vm, 'buffers', None),
            "cached": getattr(vm, 'cached', None),
            "shared": getattr(vm, 'shared', None),
        }

    def get_swap_memory(self) -> Dict[str, any]:
        """Get swap memory information."""
        sm = psutil.swap_memory()
        return {
            "total": sm.total,
            "used": sm.used,
            "free": sm.free,
            "percent": sm.percent,
            "sin": sm.sin,
            "sout": sm.sout,
        }

    def get_memory_percent(self) -> float:
        """Get memory usage percentage."""
        return psutil.virtual_memory().percent

    def get_swap_percent(self) -> float:
        """Get swap usage percentage."""
        return psutil.swap_memory().percent
