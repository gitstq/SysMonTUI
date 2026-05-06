"""CPU monitoring module."""
import psutil
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class CPUInfo:
    """CPU information data class."""
    percent: float
    percent_per_cpu: List[float]
    freq_current: Optional[float]
    freq_min: Optional[float]
    freq_max: Optional[float]
    core_count: int
    thread_count: int
    cpu_count_physical: int
    cpu_count_logical: int
    ctx_switches: int
    interrupts: int
    soft_interrupts: int
    syscalls: int


class CPUMonitor:
    """Monitor CPU usage and information."""

    def __init__(self):
        self._prev_cpu_times = None

    def get_info(self) -> CPUInfo:
        """Get comprehensive CPU information."""
        # Get CPU percent (overall and per core)
        percent = psutil.cpu_percent(interval=None)
        percent_per_cpu = psutil.cpu_percent(interval=None, percpu=True)

        # Get CPU frequency
        freq = psutil.cpu_freq()
        freq_current = freq.current if freq else None
        freq_min = freq.min if freq else None
        freq_max = freq.max if freq else None

        # Get CPU counts
        cpu_count_physical = psutil.cpu_count(logical=False) or 1
        cpu_count_logical = psutil.cpu_count(logical=True) or 1

        # Get CPU stats
        cpu_stats = psutil.cpu_stats()

        return CPUInfo(
            percent=percent,
            percent_per_cpu=percent_per_cpu,
            freq_current=freq_current,
            freq_min=freq_min,
            freq_max=freq_max,
            core_count=cpu_count_physical,
            thread_count=cpu_count_logical,
            cpu_count_physical=cpu_count_physical,
            cpu_count_logical=cpu_count_logical,
            ctx_switches=cpu_stats.ctx_switches,
            interrupts=cpu_stats.interrupts,
            soft_interrupts=cpu_stats.soft_interrupts,
            syscalls=cpu_stats.syscalls,
        )

    def get_percent(self) -> float:
        """Get overall CPU usage percentage."""
        return psutil.cpu_percent(interval=None)

    def get_per_cpu_percent(self) -> List[float]:
        """Get CPU usage percentage for each core."""
        return psutil.cpu_percent(interval=None, percpu=True)

    def get_frequency(self) -> Optional[Tuple[float, Optional[float], Optional[float]]]:
        """Get CPU frequency (current, min, max)."""
        freq = psutil.cpu_freq()
        if freq:
            return freq.current, freq.min, freq.max
        return None

    def get_load_average(self) -> Optional[Tuple[float, float, float]]:
        """Get system load average (1min, 5min, 15min).

        Returns None on Windows.
        """
        try:
            load1, load5, load15 = psutil.getloadavg()
            return load1, load5, load15
        except AttributeError:
            return None

    def get_cpu_times(self) -> Dict[str, float]:
        """Get CPU time spent in different modes."""
        times = psutil.cpu_times()
        result = {
            "user": getattr(times, "user", 0),
            "system": getattr(times, "system", 0),
            "idle": getattr(times, "idle", 0),
        }
        # Add optional fields if available
        for field in ["nice", "iowait", "irq", "softirq", "steal", "guest"]:
            if hasattr(times, field):
                result[field] = getattr(times, field)
        return result

    def get_cpu_count(self, logical: bool = True) -> int:
        """Get number of CPUs."""
        return psutil.cpu_count(logical=logical) or 1

    @staticmethod
    def get_cpu_brand() -> str:
        """Get CPU brand/model name."""
        try:
            import platform
            if hasattr(platform, 'processor'):
                proc = platform.processor()
                if proc:
                    return proc
        except:
            pass

        # Try to get from /proc/cpuinfo on Linux
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line.startswith('model name'):
                        return line.split(':')[1].strip()
        except:
            pass

        return "Unknown CPU"
