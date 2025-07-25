from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from shum.ads.api.views import AdViewSet
from shum.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("ads", AdViewSet)

app_name = "api"
urlpatterns = router.urls
