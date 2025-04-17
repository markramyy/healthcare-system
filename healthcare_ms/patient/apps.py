from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PatientConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "healthcare_ms.patient"
    verbose_name = _("Patient Management")

    def ready(self):
        try:
            import healthcare_ms.patient.signals  # noqa: F401
        except ImportError:
            pass
