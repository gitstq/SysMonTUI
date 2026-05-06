"""History data management for monitoring."""
from collections import deque
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DataPoint:
    """Single data point with timestamp."""
    timestamp: float
    value: float


class RingBuffer:
    """Fixed-size ring buffer for storing historical data."""

    def __init__(self, size: int = 60):
        self.size = size
        self._buffer: deque = deque(maxlen=size)

    def append(self, value: float) -> None:
        """Add a new value to the buffer."""
        self._buffer.append(DataPoint(datetime.now().timestamp(), value))

    def get_values(self) -> List[float]:
        """Get all values as a list."""
        return [dp.value for dp in self._buffer]

    def get_data_points(self) -> List[DataPoint]:
        """Get all data points."""
        return list(self._buffer)

    def get_latest(self) -> Optional[float]:
        """Get the latest value."""
        if self._buffer:
            return self._buffer[-1].value
        return None

    def get_average(self) -> Optional[float]:
        """Get the average of all values."""
        if not self._buffer:
            return None
        return sum(dp.value for dp in self._buffer) / len(self._buffer)

    def get_max(self) -> Optional[float]:
        """Get the maximum value."""
        if not self._buffer:
            return None
        return max(dp.value for dp in self._buffer)

    def get_min(self) -> Optional[float]:
        """Get the minimum value."""
        if not self._buffer:
            return None
        return min(dp.value for dp in self._buffer)

    def clear(self) -> None:
        """Clear all data."""
        self._buffer.clear()

    def __len__(self) -> int:
        return len(self._buffer)


class HistoryManager:
    """Manage history data for multiple metrics."""

    def __init__(self, buffer_size: int = 60):
        self.buffer_size = buffer_size
        self._buffers: dict = {}

    def get_buffer(self, name: str) -> RingBuffer:
        """Get or create a buffer for a metric."""
        if name not in self._buffers:
            self._buffers[name] = RingBuffer(self.buffer_size)
        return self._buffers[name]

    def record(self, name: str, value: float) -> None:
        """Record a value for a metric."""
        buffer = self.get_buffer(name)
        buffer.append(value)

    def get_values(self, name: str) -> List[float]:
        """Get all values for a metric."""
        return self.get_buffer(name).get_values()

    def get_latest(self, name: str) -> Optional[float]:
        """Get the latest value for a metric."""
        return self.get_buffer(name).get_latest()

    def clear(self, name: Optional[str] = None) -> None:
        """Clear buffer(s)."""
        if name:
            if name in self._buffers:
                self._buffers[name].clear()
        else:
            for buffer in self._buffers.values():
                buffer.clear()
