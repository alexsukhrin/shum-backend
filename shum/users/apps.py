import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "shum.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import shum.users.signals  # noqa: F401, PLC0415
