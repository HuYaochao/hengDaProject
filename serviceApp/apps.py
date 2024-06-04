from django.apps import AppConfig # type: ignore


class ServiceappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "serviceApp"
    verbose_name = '资料'
