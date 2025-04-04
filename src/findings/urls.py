from django.urls import include, path
from rest_framework import routers

from .views import FindingView

router = routers.DefaultRouter()
router.register(r"findings", FindingView, "Findings")


urlpatterns = [
    path("", include(router.urls)),
]
