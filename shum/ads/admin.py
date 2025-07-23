from django.contrib import admin
from django.utils.html import format_html

from shum.ads.models import Ad
from shum.ads.models import AdImage


class AdImageInline(admin.TabularInline):
    """Inline admin for ad images."""

    model = AdImage
    extra = 1
    fields = ["image", "alt_text", "order", "image_preview"]
    readonly_fields = ["image_preview"]

    @admin.display(
        description="Preview",
    )
    def image_preview(self, obj):
        """Show image preview in admin."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image.url,
            )
        return "No image"


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Admin for Ad model."""

    list_display = [
        "title",
        "owner",
        "price",
        "is_active",
        "is_sold",
        "main_image_preview",
        "created_at",
    ]
    list_filter = ["is_active", "is_sold", "created_at", "updated_at"]
    search_fields = ["title", "description", "owner__email"]
    list_editable = ["is_active", "is_sold"]
    inlines = [AdImageInline]

    fields = [
        "title",
        "description",
        "price",
        "is_active",
        "is_sold",
        "owner",
    ]

    @admin.display(
        description="Image",
    )
    def main_image_preview(self, obj):
        """Show main image preview in list."""
        main_image = obj.main_image
        if main_image:
            return format_html(
                '<img src="{}" style="max-height: 40px; max-width: 40px;" />',
                main_image.image.url,
            )
        return "No image"


@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    """Admin for AdImage model."""

    list_display = ["ad", "image_preview", "alt_text", "order", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["ad__title", "alt_text"]
    list_editable = ["order"]

    @admin.display(
        description="Preview",
    )
    def image_preview(self, obj):
        """Show image preview in list."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image.url,
            )
        return "No image"
