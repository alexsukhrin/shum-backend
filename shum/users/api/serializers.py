from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from shum.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["id", "email", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with additional user data."""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom user data to response
        data.update({
            'user': {
                'id': self.user.id,
                'email': self.user.email,
                'name': self.user.name,
            }
        })
        
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration with JWT tokens."""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "email", "name", "password", "password_confirm", "tokens"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        # Remove password_confirm from validated_data
        validated_data.pop("password_confirm")
        
        # Create user
        user = User.objects.create_user(**validated_data)
        
        return user
    
    def get_tokens(self, obj):
        """Generate JWT tokens for the created user."""
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.'
                )
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
                
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".'
            )
