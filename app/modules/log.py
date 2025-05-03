import functools
import logging
import time
from typing import Callable, Awaitable, Any

logger = logging.getLogger(__name__)

def log_async(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        logger.info(f"[CALL] {func.__name__} called with args={args[1:]}, kwargs={kwargs}")
        try:
            result = await func(*args, **kwargs)
            duration = (time.time() - start) * 1000
            logger.info(f"[SUCCESS] {func.__name__} returned in {duration:.2f}ms")
            return result
        except Exception as e:
            logger.exception(f"[ERROR] {func.__name__} failed with error: {e}")
            raise
    return wrapper