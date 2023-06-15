from time import perf_counter
import threading


class Metrics:
    def __init__(self):
        self.lock = threading.Lock()
        self.start_time = 0
        self.messages_received = 0

    def increase(self):
        with self.lock:
            if self.start_time == 0:
                self.start_time = perf_counter()

            # Reset every minute to have better understanding of performance
            elif (perf_counter() - self.start_time) >= 60:
                self.start_time = perf_counter()
                self.messages_received = 0

            self.messages_received += 1

    @property
    def message_rate(self) -> float:
        with self.lock:
            end_time = perf_counter()

            elapsed = end_time - self.start_time
            messages_per_second = self.messages_received / elapsed

        return messages_per_second

    def end(self) -> float:
        messages_per_second = self.message_rate

        self.reset()

        return messages_per_second

    def reset(self):
        with self.lock:
            self.start_time = 0
            self.messages_received = 0
