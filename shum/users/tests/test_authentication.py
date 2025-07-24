import pytest
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from shum.users.api.serializers import UserLoginSerializer
from shum.users.api.serializers import UserRegistrationSerializer

User = get_user_model()


@pytest.mark.django_db
class TestEmailAuthentication:
    """Test email-based authentication configuration."""

    def test_user_model_configuration(self):
        """Test that User model is correctly configured for email authentication."""
        # USERNAME_FIELD should be email
        assert User.USERNAME_FIELD == "email"

        # username field should be None
        user = User()
        assert not hasattr(user, "username") or user.username is None

        # REQUIRED_FIELDS should be empty since email is the username
        assert User.REQUIRED_FIELDS == []

    def test_create_user_with_email(self):
        """Test creating user with email as username."""
        email = "test@example.com"
        password = "testpass123"  # noqa: S105

        user = User.objects.create_user(email=email, password=password)

        assert user.email == email
        assert user.check_password(password)
        assert user.username is None

    def test_authenticate_with_email_parameter(self):
        """Test authentication using email parameter."""
        email = "test@example.com"
        password = "testpass123"  # noqa: S105

        user = User.objects.create_user(email=email, password=password)

        # Authenticate with email parameter (new way)
        auth_user = authenticate(email=email, password=password)
        assert auth_user is not None
        assert auth_user.id == user.id

    def test_authenticate_with_username_parameter_still_works(self):
        """Test authentication with username parameter for backwards compatibility."""
        email = "test@example.com"
        password = "testpass123"  # noqa: S105

        user = User.objects.create_user(email=email, password=password)

        # Authenticate with username parameter (old way, should still work)
        auth_user = authenticate(username=email, password=password)
        assert auth_user is not None
        assert auth_user.id == user.id

    def test_api_login_with_email(self):
        """Test API login endpoint uses email correctly."""
        email = "test@example.com"
        password = "testpass123"  # noqa: S105

        User.objects.create_user(email=email, password=password)

        client = APIClient()
        response = client.post(
            "/api/auth/login/",
            {"email": email, "password": password},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert "user" in response.data
        assert "tokens" in response.data
        assert response.data["user"]["email"] == email
        assert "access" in response.data["tokens"]
        assert "refresh" in response.data["tokens"]

    def test_jwt_token_contains_correct_user_id(self):
        """Test that JWT tokens contain correct user_id claim."""
        email = "test@example.com"
        password = "testpass123"  # noqa: S105

        user = User.objects.create_user(email=email, password=password)

        client = APIClient()
        response = client.post(
            "/api/auth/token/",
            {"email": email, "password": password},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

        # Use the token to access protected endpoint
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        profile_response = client.get("/api/auth/profile/")

        assert profile_response.status_code == status.HTTP_200_OK
        assert profile_response.data["id"] == user.id
        assert profile_response.data["email"] == email

    def test_api_registration_returns_user_and_tokens(self):
        """Test API registration endpoint returns complete user data and tokens."""
        email = "newuser@example.com"
        password = "testpass123"  # noqa: S105
        first_name = "John"
        last_name = "Doe"

        client = APIClient()
        response = client.post(
            "/api/auth/register/",
            {
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.data
        assert "tokens" in response.data

        # Check user data
        user_data = response.data["user"]
        assert user_data["email"] == email
        assert user_data["first_name"] == first_name
        assert user_data["last_name"] == last_name
        assert user_data["name"] == f"{first_name} {last_name}"

        # Check tokens
        tokens = response.data["tokens"]
        assert "access" in tokens
        assert "refresh" in tokens

        # Verify user was created in database
        user = User.objects.get(email=email)
        assert user.name == f"{first_name} {last_name}"

    def test_login_serializer_consolidates_token_generation(self):
        """Test that login serializer handles complete response generation."""
        email = "test@example.com"
        password = "testpass123"  # noqa: S105
        user_name = "Test User"

        user = User.objects.create_user(email=email, password=password, name=user_name)

        serializer = UserLoginSerializer(data={"email": email, "password": password})
        assert serializer.is_valid()

        # The validated_data should contain complete structure
        data = serializer.validated_data
        assert "user" in data
        assert "tokens" in data

        assert data["user"]["id"] == user.id
        assert data["user"]["email"] == email
        assert data["user"]["name"] == user_name
        assert "access" in data["tokens"]
        assert "refresh" in data["tokens"]

    def test_registration_serializer_consolidates_token_generation(self):
        """Test that registration serializer handles complete response generation."""
        email = "newuser@example.com"
        password = "testpass123"  # noqa: S105
        first_name = "Jane"
        last_name = "Smith"

        serializer = UserRegistrationSerializer(
            data={
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
        assert serializer.is_valid()

        # The save() method should return complete structure
        data = serializer.save()
        assert "user" in data
        assert "tokens" in data

        user_data = data["user"]
        assert user_data["email"] == email
        assert user_data["first_name"] == first_name
        assert user_data["last_name"] == last_name
        assert user_data["name"] == f"{first_name} {last_name}"

        tokens = data["tokens"]
        assert "access" in tokens
        assert "refresh" in tokens

        # Verify user was created
        user = User.objects.get(email=email)
        assert user.name == f"{first_name} {last_name}"
