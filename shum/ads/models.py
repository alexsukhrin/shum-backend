from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def ad_image_path(instance, filename):
    """Generate upload path for ad images."""
    return f"ads/ad_{instance.ad.id}/{filename}"


class Ad(models.Model):
    """Ad model for marketplace - user creates ads to sell items."""

    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_sold = models.BooleanField(_("Is Sold"), default=False)

    # Relations
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ads",
        verbose_name=_("Owner"),
    )

    # Timestamps
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Ad")
        verbose_name_plural = _("Ads")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def main_image(self):
        """Get the first image as main image."""
        return self.images.first()


class AdImage(models.Model):
    """Ad image model with S3 storage."""

    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Ad"),
    )

    image = models.ImageField(
        _("Image"),
        upload_to=ad_image_path,
        help_text=_("Ad image (stored in S3)"),
    )

    alt_text = models.CharField(
        _("Alt Text"),
        max_length=255,
        blank=True,
        help_text=_("Alternative text for image accessibility"),
    )

    order = models.PositiveIntegerField(_("Order"), default=0)

    # Timestamps
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Ad Image")
        verbose_name_plural = _("Ad Images")
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"{self.ad.title} - Image {self.order}"
