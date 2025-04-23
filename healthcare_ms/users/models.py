from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from healthcare_ms.core.models import DBBase


class User(AbstractUser, DBBase):
    """
    Custom User model that extends Django's AbstractUser and our DBBase model.
    """
    USER_TYPE_CHOICES = (
        ('admin', _('Administrator')),
        ('doctor', _('Doctor')),
        ('patient', _('Patient')),
        ('staff', _('Staff')),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='patient', verbose_name=_('User Type'))
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Phone Number'))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('Date of Birth'))
    address = models.TextField(blank=True, null=True, verbose_name=_('Address'))
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name=_('Profile Picture'))
    is_verified = models.BooleanField(default=False, verbose_name=_('Is Verified'))

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created']

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def get_user_type_display(self):
        return dict(self.USER_TYPE_CHOICES).get(self.user_type, self.user_type)
