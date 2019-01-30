"""
app configuration
"""
from django.apps import AppConfig


class SolutionsAppProgressConfig(AppConfig):

    name = 'openedx.core.djangoapps.youngsphere.progress'
    verbose_name = 'progress app'
    label = 'progress'

    def ready(self):

        # import signal handlers
        import openedx.core.djangoapps.youngsphere.progress.signals  # pylint: disable=unused-import
