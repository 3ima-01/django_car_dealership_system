from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Accounts
from apps.accounts.api.views.accounts import AccountsViewSet

# AutoShows
from apps.autoshows.api.views.autoshows import AutoShowsViewSet
from apps.autoshows.api.views.discount import DiscountViewSet as AutoShowDiscountViewSet
from apps.autoshows.api.views.stock import AutoShowsStockViewSet

# Cars
from apps.cars.api.views.cars import CarsViewSet

# Customers
from apps.customers.api.views.offers import OffersViewSet
from apps.customers.api.views.profiles import ProfileViewSet
from apps.suppliers.api.views.discount import DiscountViewSet as SuppliersDiscountViewSet
from apps.suppliers.api.views.stock import SuppliersStockViewSet

# Suppliers
from apps.suppliers.api.views.suppliers import SuppliersViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Car Dealership Sysytem API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = SimpleRouter()
router.register(r"cars", CarsViewSet, basename="cars")
router.register(r"accounts", AccountsViewSet, basename="accounts")
# Customers
router.register(r"offers", OffersViewSet, basename="offers")
router.register(r"profiles", ProfileViewSet, basename="profiles")
# Suppliers
router.register(r"suppliers", SuppliersViewSet, basename="suppliers")

suppliers_router = routers.NestedSimpleRouter(router, r"suppliers", lookup="supplier")
suppliers_router.register(r"stock", SuppliersStockViewSet, basename="supplier-stock")
suppliers_router.register(r"discount", SuppliersDiscountViewSet, basename="supplier-discount")
# AutoShows
router.register(r"autoshows", AutoShowsViewSet, basename="autoshows")

autoshows_router = routers.NestedSimpleRouter(router, r"autoshows", lookup="autoshow")
autoshows_router.register(r"stock", AutoShowsStockViewSet, basename="autoshow-stock")
autoshows_router.register(r"discount", AutoShowDiscountViewSet, basename="autoshow-discount")


urlpatterns = [
    path("admin/", admin.site.urls),
    # JWT
    path("api/v1/accounts/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/accounts/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ViewSets
    path("api/v1/", include(router.urls)),
    path("api/v1/", include(suppliers_router.urls)),
    path("api/v1/", include(autoshows_router.urls)),
    # Swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
