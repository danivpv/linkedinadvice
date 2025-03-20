import logging
import time
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

logger = logging.getLogger("career-advisor")


# API usage monitoring
class APIMonitor:
    """Monitors API usage to prevent abuse and track costs"""

    def __init__(self):
        self.request_count = 0
        self.last_reset = time.time()
        self.daily_limit = 100  # Adjust based on your budget

    def check_limit(self):
        """Check if the API request limit has been reached"""
        # Reset counter if a new day has begun
        current_time = time.time()
        if (current_time - self.last_reset) > 86400:  # 24 hours
            self.request_count = 0
            self.last_reset = current_time

        return self.request_count < self.daily_limit

    def log_request(self, user_input_length):
        """Log an API request and increment counter"""
        self.request_count += 1
        logger.info(
            f"API request #{self.request_count}. Input length: {user_input_length} chars"
        )


def monitor_api(func):
    """Decorator to monitor API usage"""
    api_monitor = APIMonitor()

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not api_monitor.check_limit():
            return "Daily request limit reached. Please try again tomorrow."

        # Estimate input size from args and kwargs
        input_size = sum(len(str(arg)) for arg in args) + sum(
            len(str(v)) for v in kwargs.values()
        )
        api_monitor.log_request(input_size)

        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time

        logger.info(f"Request completed in {elapsed:.2f} seconds")
        return result

    return wrapper
