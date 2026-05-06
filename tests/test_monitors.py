"""Unit tests for monitor modules."""
import unittest
from sysmontui.monitors import CPUMonitor, MemoryMonitor, DiskMonitor, NetworkMonitor, ProcessMonitor


class TestCPUMonitor(unittest.TestCase):
    """Test CPU monitor."""

    def setUp(self):
        self.monitor = CPUMonitor()

    def test_get_percent(self):
        """Test getting CPU percentage."""
        percent = self.monitor.get_percent()
        self.assertIsInstance(percent, float)
        self.assertGreaterEqual(percent, 0.0)
        self.assertLessEqual(percent, 100.0)

    def test_get_per_cpu_percent(self):
        """Test getting per-CPU percentages."""
        percents = self.monitor.get_per_cpu_percent()
        self.assertIsInstance(percents, list)
        self.assertGreater(len(percents), 0)
        for p in percents:
            self.assertIsInstance(p, float)
            self.assertGreaterEqual(p, 0.0)
            self.assertLessEqual(p, 100.0)

    def test_get_info(self):
        """Test getting CPU info."""
        info = self.monitor.get_info()
        self.assertIsNotNone(info)
        self.assertIsInstance(info.percent, float)
        self.assertIsInstance(info.core_count, int)
        self.assertIsInstance(info.thread_count, int)

    def test_get_cpu_count(self):
        """Test getting CPU count."""
        logical = self.monitor.get_cpu_count(logical=True)
        physical = self.monitor.get_cpu_count(logical=False)
        self.assertIsInstance(logical, int)
        self.assertIsInstance(physical, int)
        self.assertGreaterEqual(logical, physical)


class TestMemoryMonitor(unittest.TestCase):
    """Test memory monitor."""

    def setUp(self):
        self.monitor = MemoryMonitor()

    def test_get_info(self):
        """Test getting memory info."""
        info = self.monitor.get_info()
        self.assertIsNotNone(info)
        self.assertIsInstance(info.total, int)
        self.assertIsInstance(info.used, int)
        self.assertIsInstance(info.percent, float)
        self.assertGreater(info.total, 0)

    def test_get_memory_percent(self):
        """Test getting memory percentage."""
        percent = self.monitor.get_memory_percent()
        self.assertIsInstance(percent, float)
        self.assertGreaterEqual(percent, 0.0)
        self.assertLessEqual(percent, 100.0)

    def test_get_virtual_memory(self):
        """Test getting virtual memory info."""
        vm = self.monitor.get_virtual_memory()
        self.assertIsInstance(vm, dict)
        self.assertIn("total", vm)
        self.assertIn("used", vm)
        self.assertIn("percent", vm)


class TestDiskMonitor(unittest.TestCase):
    """Test disk monitor."""

    def setUp(self):
        self.monitor = DiskMonitor()

    def test_get_partitions(self):
        """Test getting disk partitions."""
        partitions = self.monitor.get_partitions()
        self.assertIsInstance(partitions, list)
        # Should have at least root partition
        self.assertGreater(len(partitions), 0)

    def test_get_usage(self):
        """Test getting disk usage."""
        usage = self.monitor.get_usage("/")
        self.assertIsNotNone(usage)
        self.assertIn("total", usage)
        self.assertIn("used", usage)
        self.assertIn("percent", usage)


class TestNetworkMonitor(unittest.TestCase):
    """Test network monitor."""

    def setUp(self):
        self.monitor = NetworkMonitor()

    def test_get_interfaces(self):
        """Test getting network interfaces."""
        interfaces = self.monitor.get_interfaces()
        self.assertIsInstance(interfaces, list)

    def test_get_io_counters(self):
        """Test getting I/O counters."""
        counters = self.monitor.get_io_counters()
        if counters:
            self.assertIsInstance(counters, dict)

    def test_get_connection_count(self):
        """Test getting connection count."""
        count = self.monitor.get_connection_count()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)


class TestProcessMonitor(unittest.TestCase):
    """Test process monitor."""

    def setUp(self):
        self.monitor = ProcessMonitor()

    def test_get_processes(self):
        """Test getting process list."""
        processes = self.monitor.get_processes(limit=10)
        self.assertIsInstance(processes, list)
        self.assertLessEqual(len(processes), 10)

    def test_get_process_count(self):
        """Test getting process count."""
        count = self.monitor.get_process_count()
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)

    def test_get_top_cpu_processes(self):
        """Test getting top CPU processes."""
        processes = self.monitor.get_top_cpu_processes(limit=5)
        self.assertIsInstance(processes, list)
        self.assertLessEqual(len(processes), 5)


if __name__ == "__main__":
    unittest.main()
