from django.apps import AppConfig


class StoresConfig(AppConfig):
    name = 'Stores'
    verbose_name = 'stores'

    
    def ready(self):
        import Stores.signals.handlers

