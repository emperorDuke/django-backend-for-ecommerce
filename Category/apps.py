from django.apps import AppConfig


class CategoryConfig(AppConfig):
    name = 'Category'
    verbose_name = 'Category'

    def ready(self):
        import Category.signals.handlers
