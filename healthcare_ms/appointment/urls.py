from django.urls import path
from . import views

app_name = 'appointment'

urlpatterns = [
    # Appointment Type URLs
    path('types/', views.appointment_type_list, name='appointment-type-list'),
    path('types/<uuid:guid>/', views.appointment_type_detail, name='appointment-type-detail'),
    path('types/create/', views.appointment_type_create, name='appointment-type-create'),
    path('types/<uuid:guid>/update/', views.appointment_type_update, name='appointment-type-update'),

    # Appointment Slot URLs
    path('slots/', views.appointment_slot_list, name='appointment-slot-list'),
    path('slots/<uuid:guid>/', views.appointment_slot_detail, name='appointment-slot-detail'),
    path('slots/create/', views.appointment_slot_create, name='appointment-slot-create'),
    path('slots/<uuid:guid>/update/', views.appointment_slot_update, name='appointment-slot-update'),

    # Appointment URLs
    path('', views.appointment_list, name='appointment-list'),
    path('<uuid:guid>/', views.appointment_detail, name='appointment-detail'),
    path('create/', views.appointment_create, name='appointment-create'),
    path('<uuid:guid>/update/', views.appointment_update, name='appointment-update'),
]
