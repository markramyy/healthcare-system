from django.contrib import admin

from healthcare_ms.patient.models import PatientProfile, Insurance, EmergencyContact


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'height', 'weight', 'primary_doctor')
    list_filter = ('blood_type',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name',
                     'primary_doctor__username', 'primary_doctor__first_name', 'primary_doctor__last_name')
    raw_id_fields = ('user', 'primary_doctor')


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'policy_number', 'coverage_start_date', 'coverage_end_date', 'is_active')
    list_filter = ('provider', 'is_active', 'coverage_start_date', 'coverage_end_date')
    search_fields = ('provider', 'policy_number', 'group_number', 'patient__username')
    date_hierarchy = 'coverage_start_date'
    raw_id_fields = ('patient',)


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('patient', 'name', 'relationship', 'phone_number', 'is_primary')
    list_filter = ('relationship', 'is_primary')
    search_fields = ('name', 'phone_number', 'email', 'patient__username')
    raw_id_fields = ('patient',)
