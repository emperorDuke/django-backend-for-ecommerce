from django.apps import AppConfig


class RatingsConfig(AppConfig):
    name = 'Ratings'
    verbose_name = 'ratings'

    def ready(self):
        import Ratings.signals.handlers
