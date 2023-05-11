from django.apps import AppConfig

#a esto hace referencia apps en settings
class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
