from rest_framework.routers import DefaultRouter
from healthcare_ms.appointment.api import (
    AppointmentTypeViewSet,
    AppointmentSlotViewSet,
    AppointmentViewSet
)

router = DefaultRouter()
router.register(r'appointment-types', AppointmentTypeViewSet, basename='appointment-type')
router.register(r'appointment-slots', AppointmentSlotViewSet, basename='appointment-slot')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = router.urls
