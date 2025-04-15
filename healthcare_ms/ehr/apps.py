from django.apps import AppConfig


class EhrConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "healthcare_ms.ehr"

    def ready(self):
        try:
            import healthcare_ms.ehr.signals  # noqa: F401
        except ImportError:
            pass
