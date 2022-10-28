from django.apps import AppConfig


class ChongzhiConfig(AppConfig):
    name = 'chongzhi'
    def ready(self):
        # improt signal handlers
        import chongzhi.signals