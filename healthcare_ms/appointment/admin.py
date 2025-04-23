from django.contrib import admin

from healthcare_ms.appointment.models import AppointmentType, AppointmentSlot, Appointment


@admin.register(AppointmentType)
class AppointmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


@admin.register(AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'is_available')
    list_filter = ('date', 'is_available')
    search_fields = ('doctor__username', 'doctor__first_name', 'doctor__last_name')
    date_hierarchy = 'date'
    raw_id_fields = ('doctor',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_type', 'slot', 'appointment_status')
    list_filter = ('appointment_status', 'appointment_type', 'slot__date')
    search_fields = ('patient__username', 'patient__first_name', 'patient__last_name',
                     'doctor__username', 'doctor__first_name', 'doctor__last_name',
                     'reason', 'notes')
    date_hierarchy = 'slot__date'
    raw_id_fields = ('patient', 'doctor', 'appointment_type', 'slot')
