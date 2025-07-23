from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.db.models import ImageField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


def user_avatar_path(instance, filename):
    """Generate upload path for user avatars."""
    return f"avatars/user_{instance.id}/{filename}"


class User(AbstractUser):
    """
    Default custom user model for shum.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    # Avatar stored in S3
    avatar = ImageField(
        _("Avatar"),
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        help_text=_("User profile picture (stored in S3)"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    @property
    def active_ads_count(self):
        """Get count of user's active ads."""
        return self.ads.filter(is_active=True, is_sold=False).count()
