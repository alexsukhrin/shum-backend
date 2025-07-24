from django.db import models
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from shum.ads.api.serializers import AdCreateSerializer
from shum.ads.api.serializers import AdImageSerializer
from shum.ads.api.serializers import AdSerializer
from shum.ads.models import Ad


@extend_schema_view(
    list=extend_schema(description="List all ads", tags=["Ads"]),
    retrieve=extend_schema(description="Get ad details", tags=["Ads"]),
    create=extend_schema(description="Create new ad", tags=["Ads"]),
    update=extend_schema(description="Update ad", tags=["Ads"]),
    partial_update=extend_schema(description="Partially update ad", tags=["Ads"]),
    destroy=extend_schema(description="Delete ad", tags=["Ads"]),
)
class AdViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """ViewSet for Ad model with S3 image support."""

    queryset = Ad.objects.select_related("owner").prefetch_related("images")
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == "create":
            return AdCreateSerializer
        return AdSerializer

    def get_queryset(self):
        """Filter ads based on user permissions."""
        queryset = super().get_queryset()

        # Only show active ads for non-owners
        if self.action in ["list", "retrieve"]:
            if self.request.user.is_authenticated:
                # Show all own ads, only active others
                return queryset.filter(
                    models.Q(owner=self.request.user) | models.Q(is_active=True),
                )
            # Show only active ads for anonymous users
            return queryset.filter(is_active=True)

        return queryset

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "image": {"type": "string", "format": "binary"},
                    "alt_text": {"type": "string"},
                    "order": {"type": "integer"},
                },
            },
        },
        responses={201: AdImageSerializer},
        description="Upload image for ad (stored in S3)",
        summary="Upload Ad Image",
        tags=["Ads"],
        examples=[
            OpenApiExample(
                "Upload Image",
                description="Upload an ad image with metadata",
                value={
                    "image": "binary_file_data",
                    "alt_text": "Product front view",
                    "order": 1,
                },
                request_only=True,
            ),
        ],
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        parser_classes=[MultiPartParser, FormParser],
    )
    def upload_image(self, request, pk=None):
        """Upload image for ad."""
        ad = self.get_object()

        # Check if user owns the ad
        if ad.owner != request.user:
            return Response(
                {"detail": "You can only upload images to your own ads."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Create ad image
        serializer = AdImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ad=ad)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: AdSerializer},
        description="Get user's own ads",
        summary="My Ads",
        tags=["Ads"],
    )
    @action(detail=False, permission_classes=[IsAuthenticated])
    def my_ads(self, request):
        """Get current user's ads."""
        ads = self.get_queryset().filter(owner=request.user)
        serializer = self.get_serializer(ads, many=True)
        return Response(serializer.data)

    @extend_schema(
        methods=["post"],
        request=None,
        responses={200: AdSerializer},
        description="Mark ad as sold",
        summary="Mark as Sold",
        tags=["Ads"],
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def mark_sold(self, request, pk=None):
        """Mark ad as sold."""
        ad = self.get_object()

        # Check if user owns the ad
        if ad.owner != request.user:
            return Response(
                {"detail": "You can only mark your own ads as sold."},
                status=status.HTTP_403_FORBIDDEN,
            )

        ad.is_sold = True
        ad.save()
        serializer = self.get_serializer(ad)
        return Response(serializer.data)
