from django.urls import path

from apps.autoshows.api.views.autoshows import AutoShowsAPIView

urlpatterns = [
    path("api/v1/auto-shows/", AutoShowsAPIView.as_view(), name="auto-shows-list"),
    path("api/v1/auto-shows/<uuid:id>/", AutoShowsAPIView.as_view(), name="auto-shows-detail"),
]
