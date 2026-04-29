"""
Fixed window counter rate limiter.

Flow:
1. `allow_request()` acquires a lock for thread-safe updates.
2. `_next_interval()` checks whether the current time window expired.
3. If expired, the window start time and counter are reset.
4. If the current count is below threshold, increment and allow.
5. Otherwise, reject until the window rolls over.

Known issue:
- Boundary burst problem: a client can send up to `threshold` requests at
    the end of one window and another `threshold` right after reset, creating
    a short spike of nearly 2x the intended rate.
"""

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
