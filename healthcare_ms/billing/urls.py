from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    # Service URLs
    path('services/', views.service_list, name='service-list'),
    path('services/create/', views.service_create, name='service-create'),
    path('services/<uuid:guid>/', views.service_detail, name='service-detail'),
    path('services/<uuid:guid>/update/', views.service_update, name='service-update'),

    # Invoice URLs
    path('invoices/', views.invoice_list, name='invoice-list'),
    path('invoices/create/', views.invoice_create, name='invoice-create'),
    path('invoices/<uuid:guid>/', views.invoice_detail, name='invoice-detail'),
    path('invoices/<uuid:guid>/update/', views.invoice_update, name='invoice-update'),

    # Invoice Item URLs
    path('invoice-items/', views.invoice_item_list, name='invoice-item-list'),
    path('invoice-items/create/', views.invoice_item_create, name='invoice-item-create'),
    path('invoice-items/<uuid:guid>/', views.invoice_item_detail, name='invoice-item-detail'),
    path('invoice-items/<uuid:guid>/update/', views.invoice_item_update, name='invoice-item-update'),

    # Payment URLs
    path('payments/', views.payment_list, name='payment-list'),
    path('payments/create/', views.payment_create, name='payment-create'),
    path('payments/<uuid:guid>/', views.payment_detail, name='payment-detail'),
    path('payments/<uuid:guid>/update/', views.payment_update, name='payment-update'),

    # Insurance Claim URLs
    path('insurance-claims/', views.insurance_claim_list, name='insurance-claim-list'),
    path('insurance-claims/create/', views.insurance_claim_create, name='insurance-claim-create'),
    path('insurance-claims/<uuid:guid>/', views.insurance_claim_detail, name='insurance-claim-detail'),
    path('insurance-claims/<uuid:guid>/update/', views.insurance_claim_update, name='insurance-claim-update'),
]
