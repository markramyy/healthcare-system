from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    # Patient Profile URLs
    path('profiles/', views.profile_list, name='profile-list'),
    path('profiles/create/', views.profile_create, name='profile-create'),
    path('profiles/<uuid:guid>/', views.profile_detail, name='profile-detail'),
    path('profiles/<uuid:guid>/update/', views.profile_update, name='profile-update'),

    # Insurance URLs
    path('insurance/', views.insurance_list, name='insurance-list'),
    path('insurance/create/', views.insurance_create, name='insurance-create'),
    path('insurance/<uuid:guid>/', views.insurance_detail, name='insurance-detail'),
    path('insurance/<uuid:guid>/update/', views.insurance_update, name='insurance-update'),

    # Emergency Contact URLs
    path('emergency-contacts/', views.emergency_contact_list, name='emergency-contact-list'),
    path('emergency-contacts/create/', views.emergency_contact_create, name='emergency-contact-create'),
    path('emergency-contacts/<uuid:guid>/', views.emergency_contact_detail, name='emergency-contact-detail'),
    path('emergency-contacts/<uuid:guid>/update/', views.emergency_contact_update, name='emergency-contact-update'),
]
