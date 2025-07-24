from django.contrib.auth import get_user_model
from drf_spectacular.openapi import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer
from .serializers import UserLoginSerializer
from .serializers import UserRegistrationSerializer
from .serializers import UserSerializer

User = get_user_model()


@extend_schema_view(
    retrieve=extend_schema(description="Get user details", tags=["Users"]),
    list=extend_schema(description="List all users", tags=["Users"]),
    update=extend_schema(description="Update user", tags=["Users"]),
    partial_update=extend_schema(description="Partially update user", tags=["Users"]),
)
class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @extend_schema(
        description="Get current user profile",
        tags=["Users"],
        responses={200: UserSerializer},
    )
    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


@extend_schema(
    description="Obtain JWT access and refresh tokens with user data",
    tags=["Authentication"],
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view with user data."""

    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    request=UserRegistrationSerializer,
    responses={
        201: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    description="Register a new user and receive JWT tokens",
    summary="User Registration",
    tags=["Authentication"],
    examples=[
        OpenApiExample(
            "Registration Example",
            value={
                "first_name": "Alexandr",
                "last_name": "Sukhryn",
                "email": "alexandrvirtual@gmail.com",
                "password": "password1986",
            },
            request_only=True,
        ),
        OpenApiExample(
            "Registration Response",
            value={
                "user": {
                    "id": 1,
                    "email": "alexandrvirtual@gmail.com",
                    "first_name": "Alexandr",
                    "last_name": "Sukhryn",
                    "name": "Alexandr Sukhryn",
                },
                "tokens": {
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                },
            },
            response_only=True,
        ),
    ],
)
class UserRegistrationView(APIView):
    """User registration endpoint that returns JWT tokens."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=UserLoginSerializer,
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    description="Login user and receive JWT tokens",
    summary="User Login",
    tags=["Authentication"],
    examples=[
        OpenApiExample(
            "Login Example",
            value={
                "email": "alexandrvirtual@gmail.com",
                "password": "password1986",
            },
            request_only=True,
        ),
        OpenApiExample(
            "Login Response",
            value={
                "user": {
                    "id": 1,
                    "email": "alexandrvirtual@gmail.com",
                    "first_name": "Alexandr",
                    "last_name": "Sukhryn",
                    "name": "Alexandr Sukhryn",
                },
                "tokens": {
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                },
            },
            response_only=True,
        ),
    ],
)
class UserLoginView(APIView):
    """User login endpoint that returns JWT tokens."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            data = serializer.validated_data
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: UserSerializer},
    description="Get current authenticated user profile",
    summary="Get User Profile",
    tags=["Users"],
)
class UserProfileView(APIView):
    """Get current user profile."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
