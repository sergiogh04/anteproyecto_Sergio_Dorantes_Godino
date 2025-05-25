from django.apps import AppConfig


class PaginaMainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pagina_main'

    def ready(self):
        import pagina_main.signals  # ✅ Correcto
