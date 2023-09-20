from django.apps import AppConfig


class BbsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bbs'

    def ready(self):
        import bbs.signals