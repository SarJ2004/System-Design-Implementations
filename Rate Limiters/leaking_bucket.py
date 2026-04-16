# Leaking Bucket Rate Limiter Flow:
# 1. Treat incoming requests as items entering a fixed-size queue (bucket).
# 2. On each new request, acquire the lock and call _consume().
# 3. _consume() computes elapsed time and removes requests at outflow_rate.
# 4. If queue length is below bucket_size, enqueue current request and allow it.
# 5. If queue is full, reject the request.

from collections import deque
import time, threading


class LeakingBucket:
    def __init__(self, bucket_size, outflow_rate):
        self.bucket_size = bucket_size
        self.outflow_rate = outflow_rate
        self.bucket = deque()
        self.last_checked_time = time.time()
        self.lock = threading.Lock()

    def _consume(self):
        curr_time = time.time()
        elapsed_time = curr_time - self.last_checked_time
        req_to_remove = int(elapsed_time * self.outflow_rate)
        while req_to_remove > 0 and self.bucket:
            self.bucket.popleft()
        self.last_checked_time = time.time()

    def allow_request(self):
        with self.lock:
            self._consume()
            if len(self.bucket) < self.bucket_size:
                self.bucket.append(time.time())
                return True
            else:
                return False
