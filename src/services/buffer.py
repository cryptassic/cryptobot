import threading
import collections
from time import perf_counter


class Buffer:
    def __init__(self, interval_s: int = 1):
        self.lock = threading.Lock()

        self.epoch_start = 0
        self.interval = interval_s
        self.buffer = collections.deque()

    def add(self, item):
        with self.lock:
            if self.epoch_start == 0:
                self.epoch_start = perf_counter()

            self.buffer.append(item)

    def read(self):
        items = None

        with self.lock:
            c_time = perf_counter()
            if c_time - self.epoch_start >= self.interval:
                items = list(self.buffer)

                self.buffer.clear()
                self.epoch_start = 0

        return items

    def reset(self):
        with self.lock:
            self.buffer.clear()
