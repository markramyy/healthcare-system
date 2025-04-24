import time
import logging
from django.conf import settings
from .health import http_requests_total, http_request_duration_seconds

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """
    Middleware for logging HTTP requests and collecting metrics.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start timer
        start_time = time.time()

        # Process request
        response = self.get_response(request)

        # Calculate duration
        duration = time.time() - start_time

        # Log request
        logger.info(
            f"Method: {request.method} Path: {request.path} "
            f"Status: {response.status_code} Duration: {duration:.2f}s"
        )

        # Record metrics
        if settings.PROMETHEUS_METRICS:
            http_request_duration_seconds.labels(
                method=request.method,
                endpoint=request.path
            ).observe(duration)

            http_requests_total.labels(
                method=request.method,
                endpoint=request.path,
                status=response.status_code
            ).inc()

        return response
