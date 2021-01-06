from django.apps import AppConfig

class TrackerAppConfig(AppConfig):
    name = 'project.apps.tracker'
    verbose_name = 'Donation Tracker'

default_app_config = 'project.apps.tracker.TrackerAppConfig'
