from django.apps import AppConfig


class GoorchidsCoreConfig(AppConfig):
    name = 'goorchids.core'
    label = 'goorchids_core'


default_app_config = 'goorchids.core.GoorchidsCoreConfig'
