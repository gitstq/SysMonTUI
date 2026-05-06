"""Process monitoring module."""
import psutil
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProcessInfo:
    """Process information data class."""
    pid: int
    name: str
    status: str
    cpu_percent: float
    memory_percent: float
    memory_rss: int
    memory_vms: int
    num_threads: int
    create_time: Optional[float]
    username: Optional[str]
    cmdline: List[str]
    exe: Optional[str]
    cwd: Optional[str]
    nice: Optional[int]
    io_read_bytes: Optional[int]
    io_write_bytes: Optional[int]


class ProcessMonitor:
    """Monitor system processes."""

    def __init__(self):
        self._process_cache: Dict[int, psutil.Process] = {}

    def get_processes(self, sort_by: str = "cpu", limit: int = 20) -> List[ProcessInfo]:
        """Get list of processes sorted by specified criteria."""
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent',
                                          'memory_percent', 'memory_info', 'num_threads',
                                          'create_time', 'username', 'cmdline', 'exe',
                                          'cwd', 'nice', 'io_counters']):
            try:
                pinfo = proc.info
                io_counters = pinfo.get('io_counters')

                processes.append(ProcessInfo(
                    pid=pinfo['pid'],
                    name=pinfo['name'] or "Unknown",
                    status=pinfo['status'] or "Unknown",
                    cpu_percent=pinfo['cpu_percent'] or 0.0,
                    memory_percent=pinfo['memory_percent'] or 0.0,
                    memory_rss=pinfo['memory_info'].rss if pinfo.get('memory_info') else 0,
                    memory_vms=pinfo['memory_info'].vms if pinfo.get('memory_info') else 0,
                    num_threads=pinfo['num_threads'] or 0,
                    create_time=pinfo['create_time'],
                    username=pinfo['username'],
                    cmdline=pinfo['cmdline'] or [],
                    exe=pinfo['exe'],
                    cwd=pinfo['cwd'],
                    nice=pinfo['nice'],
                    io_read_bytes=io_counters.read_bytes if io_counters else None,
                    io_write_bytes=io_counters.write_bytes if io_counters else None,
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Sort processes
        if sort_by == "cpu":
            processes.sort(key=lambda p: p.cpu_percent, reverse=True)
        elif sort_by == "memory":
            processes.sort(key=lambda p: p.memory_percent, reverse=True)
        elif sort_by == "pid":
            processes.sort(key=lambda p: p.pid)
        elif sort_by == "name":
            processes.sort(key=lambda p: p.name.lower())

        return processes[:limit]

    def get_process_count(self) -> int:
        """Get total number of processes."""
        return len(list(psutil.process_iter()))

    def get_process_count_by_status(self) -> Dict[str, int]:
        """Get process count grouped by status."""
        counts = {}
        for proc in psutil.process_iter(['status']):
            try:
                status = proc.info['status']
                counts[status] = counts.get(status, 0) + 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return counts

    def get_process_by_pid(self, pid: int) -> Optional[ProcessInfo]:
        """Get process information by PID."""
        try:
            proc = psutil.Process(pid)
            pinfo = proc.as_dict(attrs=['pid', 'name', 'status', 'cpu_percent',
                                        'memory_percent', 'memory_info', 'num_threads',
                                        'create_time', 'username', 'cmdline', 'exe',
                                        'cwd', 'nice', 'io_counters'])
            io_counters = pinfo.get('io_counters')

            return ProcessInfo(
                pid=pinfo['pid'],
                name=pinfo['name'] or "Unknown",
                status=pinfo['status'] or "Unknown",
                cpu_percent=pinfo['cpu_percent'] or 0.0,
                memory_percent=pinfo['memory_percent'] or 0.0,
                memory_rss=pinfo['memory_info'].rss if pinfo.get('memory_info') else 0,
                memory_vms=pinfo['memory_info'].vms if pinfo.get('memory_info') else 0,
                num_threads=pinfo['num_threads'] or 0,
                create_time=pinfo['create_time'],
                username=pinfo['username'],
                cmdline=pinfo['cmdline'] or [],
                exe=pinfo['exe'],
                cwd=pinfo['cwd'],
                nice=pinfo['nice'],
                io_read_bytes=io_counters.read_bytes if io_counters else None,
                io_write_bytes=io_counters.write_bytes if io_counters else None,
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None

    def kill_process(self, pid: int) -> bool:
        """Kill a process by PID."""
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def get_top_cpu_processes(self, limit: int = 10) -> List[ProcessInfo]:
        """Get top CPU consuming processes."""
        return self.get_processes(sort_by="cpu", limit=limit)

    def get_top_memory_processes(self, limit: int = 10) -> List[ProcessInfo]:
        """Get top memory consuming processes."""
        return self.get_processes(sort_by="memory", limit=limit)
