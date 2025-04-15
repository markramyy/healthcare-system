from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "healthcare_ms.users"

    def ready(self):
        try:
            import healthcare_ms.users.signals  # noqa: F401
        except ImportError:
            pass
