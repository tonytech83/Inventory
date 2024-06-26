from django.apps import AppConfig


class DevicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory.devices'

    def ready(self):
        import inventory.accounts.signals
