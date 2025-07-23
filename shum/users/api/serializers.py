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

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
            "name": {"help_text": "Full name of the user"},
            "email": {"help_text": "User's email address (used for login)"},
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
    tokens = serializers.SerializerMethodField(
        read_only=True,
        help_text="JWT access and refresh tokens",
    )

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password", "tokens"]
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

    @extend_schema_field(
        {
            "type": "object",
            "properties": {
                "refresh": {"type": "string", "description": "JWT refresh token"},
                "access": {"type": "string", "description": "JWT access token"},
            },
        },
    )
    def get_tokens(self, obj):
        """Generate JWT tokens for the created user."""
        refresh = RefreshToken.for_user(obj)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Accepts email and password, validates credentials,
    and returns user data if authentication is successful.
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
            user = authenticate(
                request=self.context.get("request"),
                username=email,
                password=password,
            )

            if not user:
                error_message = "Unable to log in with provided credentials."
                raise serializers.ValidationError(error_message)

            if not user.is_active:
                error_message = "User account is disabled."
                raise serializers.ValidationError(error_message)

            attrs["user"] = user
            return attrs
        error_message = 'Must include "email" and "password".'
        raise serializers.ValidationError(error_message)
