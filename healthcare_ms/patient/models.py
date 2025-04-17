from django.db import models
from django.utils.translation import gettext_lazy as _

from healthcare_ms.core.models import DBBase
from healthcare_ms.users.models import User


class PatientProfile(DBBase):
    GENDER_CHOICES = (
        ('male', _('Male')),
        ('female', _('Female')),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        limit_choices_to={'user_type': 'patient'},
        verbose_name=_('User')
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name=_('Gender')
    )
    blood_type = models.CharField(
        max_length=3,
        choices=(
            ('A+', 'A+'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B-', 'B-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-'),
            ('O+', 'O+'),
            ('O-', 'O-'),
        ),
        blank=True,
        null=True,
        verbose_name=_('Blood Type')
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Height (cm)')
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Weight (kg)')
    )
    allergies = models.TextField(blank=True, verbose_name=_('Allergies'))
    chronic_conditions = models.TextField(blank=True, verbose_name=_('Chronic Conditions'))
    primary_doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_patients',
        limit_choices_to={'user_type': 'doctor'},
        verbose_name=_('Primary Doctor')
    )

    class Meta:
        verbose_name = _('Patient Profile')
        verbose_name_plural = _('Patient Profiles')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.blood_type}"


class Insurance(DBBase):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='insurance_policies',
        limit_choices_to={'user_type': 'patient'},
        verbose_name=_('Patient')
    )
    provider = models.CharField(max_length=255, verbose_name=_('Insurance Provider'))
    policy_number = models.CharField(max_length=50, verbose_name=_('Policy Number'))
    group_number = models.CharField(max_length=50, blank=True, verbose_name=_('Group Number'))
    coverage_start_date = models.DateField(verbose_name=_('Coverage Start Date'))
    coverage_end_date = models.DateField(null=True, blank=True, verbose_name=_('Coverage End Date'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta:
        verbose_name = _('Insurance')
        verbose_name_plural = _('Insurance Policies')

    def __str__(self):
        return f"{self.provider} - {self.policy_number}"


class EmergencyContact(DBBase):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='emergency_contacts',
        limit_choices_to={'user_type': 'patient'},
        verbose_name=_('Patient')
    )
    name = models.CharField(max_length=255, verbose_name=_('Contact Name'))
    relationship = models.CharField(max_length=50, verbose_name=_('Relationship'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone Number'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    address = models.TextField(blank=True, verbose_name=_('Address'))
    is_primary = models.BooleanField(default=False, verbose_name=_('Is Primary Contact'))

    class Meta:
        verbose_name = _('Emergency Contact')
        verbose_name_plural = _('Emergency Contacts')

    def __str__(self):
        return f"{self.name} - {self.relationship}"
