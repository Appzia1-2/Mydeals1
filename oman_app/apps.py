from django.apps import AppConfig


class OmanAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'oman_app'

    def ready(self):
        import oman_app.signals  # Import signals when Django starts



