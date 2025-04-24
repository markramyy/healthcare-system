from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from redis import Redis
from django.conf import settings
from prometheus_client import Counter, Histogram
import time

# Prometheus metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)


def health_check(request):
    """
    Health check endpoint for Kubernetes liveness and readiness probes.
    Checks database and Redis connectivity.
    """
    start_time = time.time()

    # Check database
    db_status = "healthy"
    try:
        conn = connections['default']
        conn.cursor()
    except OperationalError:
        db_status = "unhealthy"

    # Check Redis
    redis_status = "healthy"
    try:
        redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            socket_timeout=1
        )
        redis.ping()
    except Exception:
        redis_status = "unhealthy"

    # Record metrics
    duration = time.time() - start_time
    http_request_duration_seconds.labels(
        method=request.method,
        endpoint='/health/'
    ).observe(duration)

    http_requests_total.labels(
        method=request.method,
        endpoint='/health/',
        status=200
    ).inc()

    return JsonResponse({
        "status": "healthy" if db_status == "healthy" and redis_status == "healthy" else "unhealthy",
        "database": db_status,
        "redis": redis_status,
        "version": "1.0.0"
    })
