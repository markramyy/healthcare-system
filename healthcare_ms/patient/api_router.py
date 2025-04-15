from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from healthcare_ms.patient.api import (
    PatientProfileViewSet,
    InsuranceViewSet,
    EmergencyContactViewSet
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("profiles", PatientProfileViewSet, basename="patient-profiles")
router.register("insurance", InsuranceViewSet, basename="patient-insurance")
router.register("emergency-contacts", EmergencyContactViewSet, basename="patient-emergency-contacts")

app_name = "patient"
urlpatterns = router.urls
