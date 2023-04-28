from django.conf import settings


def get_version():
    return settings.VERSION


def get_app_name():
    return settings.PROJECT_NAME


def get_default_active():
    return {'is_active': True}
