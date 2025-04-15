from django.apps import AppConfig


class BillingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "healthcare_ms.billing"

    def ready(self):
        try:
            import healthcare_ms.billing.signals  # noqa: F401
        except ImportError:
            pass
