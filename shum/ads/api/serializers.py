from drf_spectacular.openapi import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from shum.ads.models import Ad
from shum.ads.models import AdImage


class AdImageSerializer(serializers.ModelSerializer):
    """Serializer for AdImage model."""

    image_url = serializers.SerializerMethodField(
        help_text="Full URL to image stored in S3",
    )

    class Meta:
        model = AdImage
        fields = ["id", "image", "image_url", "alt_text", "order", "created_at"]
        extra_kwargs = {
            "image": {"help_text": "Ad image file (uploaded to S3)"},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        """Get full URL to image in S3."""
        if obj.image:
            return obj.image.url
        return None


class AdSerializer(serializers.ModelSerializer):
    """Serializer for Ad model."""

    images = AdImageSerializer(many=True, read_only=True)
    main_image_url = serializers.SerializerMethodField(
        help_text="URL of the main ad image",
    )
    owner_info = serializers.SerializerMethodField(
        help_text="Basic owner information",
    )

    class Meta:
        model = Ad
        fields = [
            "id",
            "title",
            "description",
            "price",
            "is_active",
            "is_sold",
            "owner",
            "owner_info",
            "images",
            "main_image_url",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "owner": {"help_text": "Ad owner user ID"},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_main_image_url(self, obj):
        """Get URL of the main ad image."""
        main_image = obj.main_image
        if main_image:
            return main_image.image.url
        return None

    @extend_schema_field(
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "email": {"type": "string"},
                "name": {"type": "string"},
            },
        },
    )
    def get_owner_info(self, obj):
        """Get basic owner information."""
        return {
            "id": obj.owner.id,
            "email": obj.owner.email,
            "name": obj.owner.name,
        }


class AdCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating ads."""

    class Meta:
        model = Ad
        fields = ["title", "description", "price", "is_active"]

    def create(self, validated_data):
        """Create ad with current user as owner."""
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
