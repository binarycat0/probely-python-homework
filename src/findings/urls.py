from django.urls import path

from .views import FindingView

urlpatterns = [
    path("findings", FindingView.as_view({"get": "retrieve"}), name="findings"),
]
