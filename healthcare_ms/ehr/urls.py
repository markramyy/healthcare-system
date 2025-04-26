from django.urls import path
from . import views

app_name = 'ehr'

urlpatterns = [
    # Medical Record URLs
    path('medical-records/', views.medical_record_list, name='medical-record-list'),
    path('medical-records/<uuid:guid>/', views.medical_record_detail, name='medical-record-detail'),
    path('medical-records/create/', views.medical_record_create, name='medical-record-create'),
    path('medical-records/<uuid:guid>/update/', views.medical_record_update, name='medical-record-update'),
    path('medical-records/<uuid:guid>/delete/', views.medical_record_delete, name='medical-record-delete'),

    # Diagnosis URLs
    path('diagnoses/', views.diagnosis_list, name='diagnosis-list'),
    path('diagnoses/<uuid:guid>/', views.diagnosis_detail, name='diagnosis-detail'),
    path('diagnoses/create/', views.diagnosis_create, name='diagnosis-create'),
    path('diagnoses/<uuid:guid>/update/', views.diagnosis_update, name='diagnosis-update'),
    path('diagnoses/<uuid:guid>/delete/', views.diagnosis_delete, name='diagnosis-delete'),

    # Treatment URLs
    path('treatments/', views.treatment_list, name='treatment-list'),
    path('treatments/<uuid:guid>/', views.treatment_detail, name='treatment-detail'),
    path('treatments/create/', views.treatment_create, name='treatment-create'),
    path('treatments/<uuid:guid>/update/', views.treatment_update, name='treatment-update'),
    path('treatments/<uuid:guid>/delete/', views.treatment_delete, name='treatment-delete'),

    # Prescription URLs
    path('prescriptions/', views.prescription_list, name='prescription-list'),
    path('prescriptions/<uuid:guid>/', views.prescription_detail, name='prescription-detail'),
    path('prescriptions/create/', views.prescription_create, name='prescription-create'),
    path('prescriptions/<uuid:guid>/update/', views.prescription_update, name='prescription-update'),
    path('prescriptions/<uuid:guid>/delete/', views.prescription_delete, name='prescription-delete'),
]
