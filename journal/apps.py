from django.apps import AppConfig


class JournalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'journal'

    def ready(self):
        from scheduler import scheduler
        scheduler.start()

