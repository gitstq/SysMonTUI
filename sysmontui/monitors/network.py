"""Network monitoring module."""
import psutil
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class NetworkInterfaceInfo:
    """Network interface information."""
    name: str
    is_up: bool
    speed: Optional[int]
    mtu: int
    duplex: Optional[str]
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int
    errin: int
    errout: int
    dropin: int
    dropout: int


@dataclass
class NetworkConnectionInfo:
    """Network connection information."""
    fd: int
    family: str
    type: str
    laddr: Optional[Tuple[str, int]]
    raddr: Optional[Tuple[str, int]]
    status: str
    pid: Optional[int]


class NetworkMonitor:
    """Monitor network usage and information."""

    def __init__(self):
        self._prev_io = None
        self._prev_time = None

    def get_io_counters(self, pernic: bool = False) -> Optional[Dict[str, any]]:
        """Get network I/O counters."""
        try:
            io_counters = psutil.net_io_counters(pernic=pernic)
            if io_counters is None:
                return None

            if pernic:
                result = {}
                for iface_name, counters in io_counters.items():
                    result[iface_name] = {
                        "bytes_sent": counters.bytes_sent,
                        "bytes_recv": counters.bytes_recv,
                        "packets_sent": counters.packets_sent,
                        "packets_recv": counters.packets_recv,
                        "errin": counters.errin,
                        "errout": counters.errout,
                        "dropin": counters.dropin,
                        "dropout": counters.dropout,
                    }
                return result
            else:
                return {
                    "total": {
                        "bytes_sent": io_counters.bytes_sent,
                        "bytes_recv": io_counters.bytes_recv,
                        "packets_sent": io_counters.packets_sent,
                        "packets_recv": io_counters.packets_recv,
                        "errin": io_counters.errin,
                        "errout": io_counters.errout,
                        "dropin": io_counters.dropin,
                        "dropout": io_counters.dropout,
                    }
                }
        except Exception:
            return None

    def get_interfaces(self) -> List[NetworkInterfaceInfo]:
        """Get network interface information."""
        interfaces = []
        io_counters = psutil.net_io_counters(pernic=True)
        iface_addrs = psutil.net_if_addrs()
        iface_stats = psutil.net_if_stats()

        for name in iface_addrs.keys():
            stats = iface_stats.get(name)
            io = io_counters.get(name) if io_counters else None

            if stats and io:
                interfaces.append(NetworkInterfaceInfo(
                    name=name,
                    is_up=stats.isup,
                    speed=stats.speed,
                    mtu=stats.mtu,
                    duplex=stats.duplex.name if hasattr(stats.duplex, 'name') else str(stats.duplex),
                    bytes_sent=io.bytes_sent,
                    bytes_recv=io.bytes_recv,
                    packets_sent=io.packets_sent,
                    packets_recv=io.packets_recv,
                    errin=io.errin,
                    errout=io.errout,
                    dropin=io.dropin,
                    dropout=io.dropout,
                ))

        return interfaces

    def get_connections(self, kind: str = "inet") -> List[NetworkConnectionInfo]:
        """Get network connections."""
        connections = []
        try:
            for conn in psutil.net_connections(kind=kind):
                family = "IPv4" if conn.family == 2 else "IPv6" if conn.family == 10 else str(conn.family)
                type_ = "TCP" if conn.type == 1 else "UDP" if conn.type == 2 else str(conn.type)

                connections.append(NetworkConnectionInfo(
                    fd=conn.fd,
                    family=family,
                    type=type_,
                    laddr=conn.laddr,
                    raddr=conn.raddr,
                    status=conn.status,
                    pid=conn.pid,
                ))
        except psutil.AccessDenied:
            pass

        return connections

    def get_connection_count(self) -> int:
        """Get total number of network connections."""
        try:
            return len(psutil.net_connections())
        except psutil.AccessDenied:
            return 0

    def calculate_speed(self, interval: float = 1.0) -> Optional[Dict[str, Tuple[float, float]]]:
        """Calculate network speed (bytes/sec).

        Returns dict with interface names as keys and (upload_speed, download_speed) as values.
        """
        import time

        io1 = psutil.net_io_counters(pernic=True)
        time1 = time.time()

        if io1 is None:
            return None

        time.sleep(interval)

        io2 = psutil.net_io_counters(pernic=True)
        time2 = time.time()

        if io2 is None:
            return None

        duration = time2 - time1
        speeds = {}

        for name in io1.keys():
            if name in io2:
                upload_speed = (io2[name].bytes_sent - io1[name].bytes_sent) / duration
                download_speed = (io2[name].bytes_recv - io1[name].bytes_recv) / duration
                speeds[name] = (upload_speed, download_speed)

        return speeds
