# Token Bucket Rate Limiter Flow:
# 1. Start with a full bucket (curr_tokens = bucket_capacity).
# 2. For each request, acquire the lock and call _refill().
# 3. _refill() adds elapsed_time * refill_rate tokens, capped at bucket_capacity.
# 4. If enough tokens are available, consume requested tokens and allow the request.
# 5. If tokens are insufficient, reject the request.
# 6. reset() restores the bucket to full capacity; peek() returns the refilled count.

import time
import threading


class TokenBucket:
    def __init__(self, bucket_capacity, refill_rate):
        self.bucket_capacity = bucket_capacity
        self.refill_rate = refill_rate
        self.curr_tokens = bucket_capacity
        self.last_refill_time = time.time()
        self.lock = threading.Lock()

    def _refill(self):
        curr_time = time.time()
        elapsed_time = curr_time - self.last_refill_time
        tokens_generated = elapsed_time * self.refill_rate
        self.curr_tokens = min(
            self.bucket_capacity, self.curr_tokens + tokens_generated
        )
        self.last_refill_time = curr_time

    def allow_request(self, tokens=1):
        with self.lock:
            self._refill()
            if self.curr_tokens >= tokens:
                self.curr_tokens -= tokens
                return True
            return False

    def reset(self):
        with self.lock:
            self.curr_tokens = self.bucket_capacity
            return self.curr_tokens

    def peek(self):
        with self.lock:
            self._refill()
            return self.curr_tokens
