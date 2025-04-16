from rest_framework.routers import DefaultRouter
from healthcare_ms.billing.api import (
    ServiceViewSet,
    InvoiceViewSet,
    InvoiceItemViewSet,
    PaymentViewSet,
    InsuranceClaimViewSet
)

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'invoice-items', InvoiceItemViewSet, basename='invoice-item')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'insurance-claims', InsuranceClaimViewSet, basename='insurance-claim')

urlpatterns = router.urls
