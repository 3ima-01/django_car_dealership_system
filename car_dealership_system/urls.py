from django.contrib import admin
from django.urls import include, path

from apps.autoshows.api.urls import urlpatterns as autoshows_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("rest_framework.urls", namespace="rest_framework")),
]

urlpatterns += autoshows_urlpatterns
