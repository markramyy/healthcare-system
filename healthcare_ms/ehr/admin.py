from django.contrib import admin

from healthcare_ms.ehr.models import MedicalRecord, Diagnosis, Treatment, Prescription


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'visit_date', 'follow_up_date')
    list_filter = ('visit_date', 'follow_up_date')
    search_fields = ('patient__username', 'patient__first_name', 'patient__last_name',
                     'doctor__username', 'doctor__first_name', 'doctor__last_name')
    date_hierarchy = 'visit_date'
    raw_id_fields = ('patient', 'doctor')


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'diagnosis_code', 'severity')
    list_filter = ('severity',)
    search_fields = ('diagnosis_code', 'description', 'medical_record__patient__username')
    raw_id_fields = ('medical_record',)


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'name', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('name', 'description', 'medical_record__patient__username')
    date_hierarchy = 'start_date'
    raw_id_fields = ('medical_record',)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'medication_name', 'dosage', 'frequency', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('medication_name', 'medical_record__patient__username')
    raw_id_fields = ('medical_record',)
