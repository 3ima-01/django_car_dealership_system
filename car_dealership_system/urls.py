from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Car Dealership Sysytem API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/", include("apps.cars.api.urls")),
    path("api/v1/", include("apps.autoshows.api.urls")),
    path("api/v1/", include("apps.suppliers.api.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]


if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
