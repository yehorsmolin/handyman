"""
URL configuration for Handyman project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from graphene_django.views import GraphQLView
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from inventory.viewsets.delivery import DeliveryViewSet
from inventory.viewsets.invoice import InvoiceViewSet
from inventory.viewsets.order import OrderViewSet
from inventory.viewsets.product import ProductViewSet
from inventory.viewsets.vendor import VendorViewSet
from inventory.viewsets.driver import DriverViewSet

from inventory.views import register, user_login, user_logout, api_authentication, home, obtain_auth_token

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('invoices', InvoiceViewSet)
router.register('orders', OrderViewSet)
router.register('vendors', VendorViewSet)
router.register('drivers', DriverViewSet)
router.register('deliveries', DeliveryViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Handyman API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="gigachadusr409@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logoutdefault/', user_logout, name='logoutdefault'),
    path('custom-auth/', api_authentication, name='api-auth'),
    path('home/', home, name='home'),
    path('obtain_token/', obtain_auth_token),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("graphql", GraphQLView.as_view(graphiql=True)),
    path("", TemplateView.as_view(template_name="index.html")),
    path("accounts/", include("allauth.urls")),
    path("logout/", LogoutView.as_view()),
]
