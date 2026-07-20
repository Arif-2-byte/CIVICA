import logging
import time

from fastapi import Request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("civica")


async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    logger.info(
        "Incoming Request | %s %s",
        request.method,
        request.url.path,
    )

    response = await call_next(request)

    process_time = (time.perf_counter() - start_time) * 1000

    logger.info(
        "Completed | %s %s | Status: %s | %.2f ms",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )

    return response