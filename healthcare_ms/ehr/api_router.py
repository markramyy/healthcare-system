from rest_framework.routers import DefaultRouter
from healthcare_ms.ehr.api import (
    MedicalRecordViewSet,
    DiagnosisViewSet,
    TreatmentViewSet,
    PrescriptionViewSet
)

router = DefaultRouter()
router.register(r'medical-records', MedicalRecordViewSet, basename='medical-record')
router.register(r'diagnoses', DiagnosisViewSet, basename='diagnosis')
router.register(r'treatments', TreatmentViewSet, basename='treatment')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = router.urls
