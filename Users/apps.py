from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'Users'
    verbose_name = 'users'

    def ready(self):
        import Users.signals.handlers
