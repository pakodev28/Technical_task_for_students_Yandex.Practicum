from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (
    EditingRightViewSet,
    OrganizationViewSet,
    RegistrationViewSet,
    WorkerViewSet,
)

router_v1 = DefaultRouter()

router_v1.register("registration", RegistrationViewSet)
router_v1.register("organizations", OrganizationViewSet)
router_v1.register(
    r"organizations/(?P<organization_id>\d+)/workers",
    WorkerViewSet,
    basename="worker",
)
router_v1.register("edit_access", EditingRightViewSet)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/api-token-auth/", views.obtain_auth_token),
]
