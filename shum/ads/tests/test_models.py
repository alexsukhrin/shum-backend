import pytest
from django.contrib.auth import get_user_model

from shum.ads.models import Ad
from shum.ads.models import AdImage

User = get_user_model()


@pytest.mark.django_db
class TestAdModel:
    def test_ad_creation(self):
        """Test basic ad creation."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )
        ad = Ad.objects.create(
            title="Test Ad",
            description="Test description",
            price="99.99",
            owner=user,
        )

        assert ad.title == "Test Ad"
        assert ad.description == "Test description"
        assert str(ad.price) == "99.99"  # Compare as string
        assert ad.owner == user
        assert ad.is_active is True
        assert ad.is_sold is False
        assert str(ad) == "Test Ad"

    def test_ad_main_image_property(self):
        """Test main_image property returns first image."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )
        ad = Ad.objects.create(
            title="Test Ad",
            owner=user,
            price="50.00",
        )

        # No images yet
        assert ad.main_image is None

        # Add image
        image = AdImage.objects.create(
            ad=ad,
            alt_text="Test image",
            order=1,
        )

        assert ad.main_image == image


@pytest.mark.django_db
class TestAdImageModel:
    def test_ad_image_creation(self):
        """Test basic ad image creation."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )
        ad = Ad.objects.create(
            title="Test Ad",
            owner=user,
            price="25.00",
        )

        image = AdImage.objects.create(
            ad=ad,
            alt_text="Test image",
            order=1,
        )

        assert image.ad == ad
        assert image.alt_text == "Test image"
        assert image.order == 1
        assert str(image) == "Test Ad - Image 1"
