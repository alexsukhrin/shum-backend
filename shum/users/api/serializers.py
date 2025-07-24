from django.contrib.auth import authenticate
from drf_spectacular.openapi import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from shum.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    """Serializer for User model with first_name and last_name extraction."""

    first_name = serializers.SerializerMethodField(
        help_text="First name extracted from name field",
    )
    last_name = serializers.SerializerMethodField(
        help_text="Last name extracted from name field",
    )
    avatar_url = serializers.SerializerMethodField(
        help_text="Full URL to user avatar stored in S3",
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "name",
            "avatar",
            "avatar_url",
            "url",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
            "name": {"help_text": "Full name of the user"},
            "email": {"help_text": "User's email address (used for login)"},
            "avatar": {"help_text": "User profile picture (uploaded to S3)"},
        }

    @extend_schema_field(OpenApiTypes.STR)
    def get_first_name(self, obj):
        """Extract first name from name field."""
        if obj.name:
            parts = obj.name.split(" ", 1)
            return parts[0] if parts else ""
        return ""

    @extend_schema_field(OpenApiTypes.STR)
    def get_last_name(self, obj):
        """Extract last name from name field."""
        if obj.name:
            parts = obj.name.split(" ", 1)
            return parts[1] if len(parts) > 1 else ""
        return ""

    @extend_schema_field(OpenApiTypes.URI)
    def get_avatar_url(self, obj):
        """Get full URL to avatar in S3."""
        if obj.avatar:
            return obj.avatar.url
        return None


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer with additional user data.

    Returns access and refresh tokens along with user information including
    first_name and last_name extracted from the name field.
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        # Split name into first_name and last_name
        name_parts = self.user.name.split(" ", 1) if self.user.name else ["", ""]
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Add custom user data to response
        data.update(
            {
                "user": {
                    "id": self.user.id,
                    "email": self.user.email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "name": self.user.name,
                },
            },
        )

        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with JWT tokens.

    Accepts first_name, last_name, email, and password.
    Combines first_name and last_name into the name field for storage.
    Returns user data and JWT tokens upon successful registration.
    """

    first_name = serializers.CharField(
        max_length=150,
        help_text="User's first name",
    )
    last_name = serializers.CharField(
        max_length=150,
        help_text="User's last name",
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Password (minimum 8 characters)",
    )

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"help_text": "User's email address (must be unique)"},
        }

    def create(self, validated_data):
        # Combine first_name and last_name into name field
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")
        name = f"{first_name} {last_name}".strip()

        validated_data["name"] = name

        # Create user
        return User.objects.create_user(**validated_data)

    def save(self, **kwargs):
        """
        Create user and return complete data structure with user info and tokens.

        Returns:
            dict: Contains 'user' and 'tokens' keys with complete user data
                  and JWT tokens
        """
        # Create the user
        user = super().save(**kwargs)

        # Split name into first_name and last_name for response
        name_parts = user.name.split(" ", 1) if user.name else ["", ""]
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": first_name,
                "last_name": last_name,
                "name": user.name,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        }


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Accepts email and password, validates credentials,
    and returns complete data structure with user info and JWT tokens.
    """

    email = serializers.EmailField(
        help_text="User's email address",
    )
    password = serializers.CharField(
        write_only=True,
        help_text="User's password",
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            # Since USERNAME_FIELD = "email", we can use email directly
            # Django's authenticate() will map this correctly to the email field
            user = authenticate(
                request=self.context.get("request"),
                email=email,  # Use email parameter directly for clarity
                password=password,
            )

            if not user:
                error_message = "Unable to log in with provided credentials."
                raise serializers.ValidationError(error_message)

            if not user.is_active:
                error_message = "User account is disabled."
                raise serializers.ValidationError(error_message)

            # Split name into first_name and last_name for response
            name_parts = user.name.split(" ", 1) if user.name else ["", ""]
            first_name = name_parts[0] if name_parts else ""
            last_name = name_parts[1] if len(name_parts) > 1 else ""

            # Generate tokens
            refresh = RefreshToken.for_user(user)

            # Return complete data structure
            return {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "name": user.name,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            }
        error_message = 'Must include "email" and "password".'
        raise serializers.ValidationError(error_message)
