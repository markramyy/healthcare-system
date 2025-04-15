from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "healthcare_ms.appointment"

    def ready(self):
        try:
            import healthcare_ms.appointment.signals  # noqa: F401
        except ImportError:
            pass
