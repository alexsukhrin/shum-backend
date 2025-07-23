import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shum.ads.models import Ad

User = get_user_model()


@pytest.mark.django_db
class TestAdAPI:
    def test_list_ads_anonymous(self):
        """Anonymous users can view active ads."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )

        # Create active and inactive ads
        Ad.objects.create(
            title="Active Ad",
            owner=user,
            price="10.00",
            is_active=True,
        )
        Ad.objects.create(
            title="Inactive Ad",
            owner=user,
            price="20.00",
            is_active=False,
        )

        client = APIClient()
        url = reverse("api:ad-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == "Active Ad"

    def test_create_ad_authenticated(self):
        """Authenticated users can create ads."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )

        client = APIClient()
        client.force_authenticate(user=user)

        url = reverse("api:ad-list")
        data = {
            "title": "New Ad",
            "description": "Test description",
            "price": "15.50",
            "is_active": True,
        }

        response = client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Ad"
        # AdCreateSerializer doesn't return owner field, so verify from DB
        created_ad = Ad.objects.get(title="New Ad")
        assert created_ad.owner == user

    def test_create_ad_unauthenticated(self):
        """Unauthenticated users cannot create ads."""
        client = APIClient()

        url = reverse("api:ad-list")
        data = {
            "title": "New Ad",
            "price": "15.50",
        }

        response = client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_my_ads_endpoint(self):
        """Test my_ads endpoint returns only user's ads."""
        user1 = User.objects.create_user(
            email="user1@example.com",
            password="testpass123",  # noqa: S106
        )
        user2 = User.objects.create_user(
            email="user2@example.com",
            password="testpass123",  # noqa: S106
        )

        # Create ads for different users
        Ad.objects.create(
            title="User1 Ad",
            owner=user1,
            price="10.00",
        )
        Ad.objects.create(
            title="User2 Ad",
            owner=user2,
            price="20.00",
        )

        client = APIClient()
        client.force_authenticate(user=user1)

        url = reverse("api:ad-my-ads")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == "User1 Ad"

    def test_mark_sold_endpoint(self):
        """Test mark_sold endpoint."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )

        ad = Ad.objects.create(
            title="Test Ad",
            owner=user,
            price="30.00",
            is_sold=False,
        )

        client = APIClient()
        client.force_authenticate(user=user)

        url = reverse("api:ad-mark-sold", kwargs={"pk": ad.pk})
        response = client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["is_sold"] is True

        # Verify in database
        ad.refresh_from_db()
        assert ad.is_sold is True
