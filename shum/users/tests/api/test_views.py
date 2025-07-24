import pytest
from rest_framework.test import APIRequestFactory

from shum.users.api.views import UserViewSet
from shum.users.models import User


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)  # type: ignore[call-arg, arg-type, misc]

        # Updated expected response to match new UserSerializer fields
        name_parts = user.name.split(" ", 1) if user.name else ["", ""]
        expected_data = {
            "id": user.pk,
            "email": user.email,
            "first_name": name_parts[0],
            "last_name": name_parts[1] if len(name_parts) > 1 else "",
            "name": user.name,
            "avatar": None,  # No avatar uploaded in test
            "avatar_url": None,  # No avatar URL in test
            "url": f"http://testserver/api/users/{user.pk}/",
        }

        assert response.data == expected_data
