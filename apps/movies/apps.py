from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.movies'
    verbose_name = 'Movies'
    
    def ready(self):
        """Initialize app when Django starts"""
        pass
