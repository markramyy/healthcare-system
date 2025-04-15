from django.db import models
from django.utils.translation import gettext_lazy as _

from healthcare_ms.core.models import DBBase
from healthcare_ms.users.models import User


class AppointmentType(DBBase):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    duration = models.PositiveIntegerField(
        help_text=_('Duration in minutes'),
        verbose_name=_('Duration')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta:
        verbose_name = _('Appointment Type')
        verbose_name_plural = _('Appointment Types')

    def __str__(self):
        return self.name


class AppointmentSlot(DBBase):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointment_slots',
        limit_choices_to={'user_type': 'doctor'},
        verbose_name=_('Doctor')
    )
    date = models.DateField(verbose_name=_('Date'))
    start_time = models.TimeField(verbose_name=_('Start Time'))
    end_time = models.TimeField(verbose_name=_('End Time'))
    is_available = models.BooleanField(default=True, verbose_name=_('Is Available'))

    class Meta:
        verbose_name = _('Appointment Slot')
        verbose_name_plural = _('Appointment Slots')
        ordering = ['date', 'start_time']
        unique_together = ['doctor', 'date', 'start_time']

    def __str__(self):
        return f"{self.doctor.get_full_name()} - {self.date} {self.start_time}"


class Appointment(DBBase):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='patient_appointments',
        limit_choices_to={'user_type': 'patient'},
        verbose_name=_('Patient')
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_appointments',
        limit_choices_to={'user_type': 'doctor'},
        verbose_name=_('Doctor')
    )
    appointment_type = models.ForeignKey(
        AppointmentType,
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name=_('Appointment Type')
    )
    slot = models.ForeignKey(
        AppointmentSlot,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name=_('Appointment Slot')
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ('scheduled', _('Scheduled')),
            ('confirmed', _('Confirmed')),
            ('in_progress', _('In Progress')),
            ('completed', _('Completed')),
            ('cancelled', _('Cancelled')),
            ('no_show', _('No Show')),
        ),
        default='scheduled',
        verbose_name=_('Status')
    )
    notes = models.TextField(blank=True, verbose_name=_('Notes'))
    reason = models.TextField(verbose_name=_('Reason for Visit'))

    class Meta:
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')
        ordering = ['-slot__date', '-slot__start_time']

    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.doctor.get_full_name()} - {self.slot.date} {self.slot.start_time}"
