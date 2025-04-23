from django.db import models
from django.utils.translation import gettext_lazy as _

from healthcare_ms.core.models import DBBase
from healthcare_ms.users.models import User


class MedicalRecord(DBBase):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='medical_records',
        limit_choices_to={'user_type': 'patient'},
        verbose_name=_('Patient')
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_medical_records',
        limit_choices_to={'user_type': 'doctor'},
        verbose_name=_('Doctor')
    )
    visit_date = models.DateTimeField(verbose_name=_('Visit Date'))
    symptoms = models.TextField(verbose_name=_('Symptoms'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))
    follow_up_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Follow Up Date'))

    class Meta:
        verbose_name = _('Medical Record')
        verbose_name_plural = _('Medical Records')
        ordering = ['-visit_date']

    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.visit_date.strftime('%B %d, %Y %I:%M %p')}"


class Diagnosis(DBBase):
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='diagnoses',
        verbose_name=_('Medical Record')
    )
    diagnosis_code = models.CharField(max_length=20, verbose_name=_('Diagnosis Code'))
    description = models.TextField(verbose_name=_('Description'))
    severity = models.CharField(
        max_length=20,
        choices=(
            ('low', _('Low')),
            ('medium', _('Medium')),
            ('high', _('High')),
            ('critical', _('Critical')),
        ),
        default='medium',
        verbose_name=_('Severity')
    )

    class Meta:
        verbose_name = _('Diagnosis')
        verbose_name_plural = _('Diagnoses')

    def __str__(self):
        return f"{self.diagnosis_code} - {self.severity}"


class Treatment(DBBase):
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='treatments',
        verbose_name=_('Medical Record')
    )
    name = models.CharField(max_length=255, verbose_name=_('Treatment Name'))
    description = models.TextField(verbose_name=_('Description'))
    start_date = models.DateTimeField(verbose_name=_('Start Date'))
    end_date = models.DateTimeField(null=True, blank=True, verbose_name=_('End Date'))
    treatment_status = models.CharField(
        max_length=20,
        choices=(
            ('planned', _('Planned')),
            ('in_progress', _('In Progress')),
            ('completed', _('Completed')),
            ('cancelled', _('Cancelled')),
        ),
        default='planned',
        verbose_name=_('Status')
    )

    class Meta:
        verbose_name = _('Treatment')
        verbose_name_plural = _('Treatments')

    def __str__(self):
        return f"{self.name} - {self.treatment_status}"


class Prescription(DBBase):
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name=_('Medical Record')
    )
    medication_name = models.CharField(max_length=255, verbose_name=_('Medication Name'))
    dosage = models.CharField(max_length=100, verbose_name=_('Dosage'))
    frequency = models.CharField(max_length=100, verbose_name=_('Frequency'))
    duration = models.CharField(max_length=100, verbose_name=_('Duration'))
    instructions = models.TextField(blank=True, verbose_name=_('Instructions'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta:
        verbose_name = _('Prescription')
        verbose_name_plural = _('Prescriptions')

    def __str__(self):
        return f"{self.medication_name} - {self.dosage}"
