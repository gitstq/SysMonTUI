"""Disk monitoring module."""
import psutil
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DiskPartitionInfo:
    """Disk partition information."""
    device: str
    mountpoint: str
    fstype: str
    opts: str
    total: int
    used: int
    free: int
    percent: float


@dataclass
class DiskIOInfo:
    """Disk I/O information."""
    read_bytes: int
    write_bytes: int
    read_count: int
    write_count: int
    read_time: int
    write_time: int


class DiskMonitor:
    """Monitor disk usage and I/O."""

    def __init__(self):
        self._prev_io = None

    def get_partitions(self, all_partitions: bool = False) -> List[DiskPartitionInfo]:
        """Get disk partition information."""
        partitions = psutil.disk_partitions(all=all_partitions)
        result = []

        for part in partitions:
            try:
                usage = psutil.disk_usage(part.mountpoint)
                result.append(DiskPartitionInfo(
                    device=part.device,
                    mountpoint=part.mountpoint,
                    fstype=part.fstype,
                    opts=part.opts,
                    total=usage.total,
                    used=usage.used,
                    free=usage.free,
                    percent=usage.percent,
                ))
            except PermissionError:
                # Skip partitions we can't access
                continue

        return result

    def get_io_counters(self, perdisk: bool = False) -> Optional[Dict[str, DiskIOInfo]]:
        """Get disk I/O counters."""
        try:
            io_counters = psutil.disk_io_counters(perdisk=perdisk)
            if io_counters is None:
                return None

            if perdisk:
                result = {}
                for disk_name, counters in io_counters.items():
                    result[disk_name] = DiskIOInfo(
                        read_bytes=counters.read_bytes,
                        write_bytes=counters.write_bytes,
                        read_count=counters.read_count,
                        write_count=counters.write_count,
                        read_time=counters.read_time,
                        write_time=counters.write_time,
                    )
                return result
            else:
                return {
                    "total": DiskIOInfo(
                        read_bytes=io_counters.read_bytes,
                        write_bytes=io_counters.write_bytes,
                        read_count=io_counters.read_count,
                        write_count=io_counters.write_count,
                        read_time=io_counters.read_time,
                        write_time=io_counters.write_time,
                    )
                }
        except Exception:
            return None

    def get_usage(self, path: str = "/") -> Optional[Dict[str, any]]:
        """Get disk usage for a specific path."""
        try:
            usage = psutil.disk_usage(path)
            return {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            }
        except Exception:
            return None

    def get_total_disk_info(self) -> Dict[str, int]:
        """Get total disk information across all partitions."""
        partitions = self.get_partitions()
        total = 0
        used = 0
        free = 0

        # Use a set to avoid counting the same device multiple times
        seen_devices = set()

        for part in partitions:
            if part.device not in seen_devices:
                seen_devices.add(part.device)
                total += part.total
                used += part.used
                free += part.free

        percent = (used / total * 100) if total > 0 else 0

        return {
            "total": total,
            "used": used,
            "free": free,
            "percent": percent,
        }
