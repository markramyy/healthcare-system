from django.apps import AppConfig


class PatientConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "healthcare_ms.patient"

    def ready(self):
        try:
            import healthcare_ms.patient.signals  # noqa: F401
        except ImportError:
            pass
