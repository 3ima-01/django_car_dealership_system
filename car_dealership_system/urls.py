from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/", include("apps.autoshows.api.urls")),
]
