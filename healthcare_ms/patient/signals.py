from django.db.models.signals import post_save
from django.dispatch import receiver
from healthcare_ms.users.models import User
from healthcare_ms.patient.models import PatientProfile
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a PatientProfile when a User with
    user_type 'patient' is created.
    """
    if created and instance.user_type == 'patient':
        try:
            # Check if a profile already exists (e.g., due to race conditions or manual creation)
            if not PatientProfile.objects.filter(user=instance).exists():
                PatientProfile.objects.create(user=instance)
                logger.info(f"PatientProfile created for user {instance.username}")
            else:
                logger.warning(f"PatientProfile already exists for user {instance.username}. Signal skipped creation.")
        except Exception as e:
            logger.error(f"Error creating PatientProfile for user {instance.username}: {e}", exc_info=True)
