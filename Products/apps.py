from django.apps import AppConfig

class ProductsConfig(AppConfig):
    name = 'Products'
    verbose_name = 'products'

    def ready(self):
        import Products.signals.handlers



