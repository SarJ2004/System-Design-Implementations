import time, threading


class FixedWindowCounter:
    def __init__(self, threshold, window_size):
        self.threshold = threshold
        self.window_size = window_size
        self.time_start = time.time()
        self.interval_requests = 0
        self.lock = threading.Lock()

    def _next_interval(self):
        now = time.time()
        if self.time_start + self.window_size <= now:
            self.time_start = now
            self.interval_requests = 0
        else:
            return

    def allow_request(self):
        with self.lock:
            self._next_interval()
            if self.interval_requests < self.threshold:
                self.interval_requests += 1
                return True
            return False
