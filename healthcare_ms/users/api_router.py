from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from healthcare_ms.users.api import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", UserViewSet, basename="users")

app_name = "users"
urlpatterns = router.urls
