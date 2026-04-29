import time, threading
from collections import deque


class SlidingWindowLogCounter:
    def __init__(self, threshold, window_size):
        self.threshold = threshold
        self.window_size = window_size
        self.time_store = deque()

    def allow_request(self):
        now = time.time()
        cutoff = (
            now - self.window_size
        )  # we need to remove all the timestamps before this cutoff value
        while self.time_store and self.time_store[0] <= cutoff:
            self.time_store.popleft()

        if len(self.time_store) < self.threshold:
            self.time_store.append(now)
            return True
        return False
