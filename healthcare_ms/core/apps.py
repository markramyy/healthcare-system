from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "healthcare_ms.core"

    def ready(self):
        try:
            import healthcare_ms.core.signals  # noqa: F401
        except ImportError:
            pass
