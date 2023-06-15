import threading
from time import perf_counter


class Buffer:
    def __init__(self, interval_ms: int = 1000):
        self.lock = threading.Lock()

        self.buffer = []
        self.interval = interval_ms

        self.epoch_start = 0

    def add(self, value):
        with self.lock:
            if self.epoch_start == 0:
                self.epoch_start = perf_counter()

            self.buffer.append(value)

    def result(self):
        result = []

        with self.lock:
            c_time = perf_counter()
            if c_time - self.epoch_start >= 1:
                result = self.buffer

                self.buffer = []
                self.epoch_start = 0

        return result

    def reset(self):
        with self.lock:
            self.buffer = []
