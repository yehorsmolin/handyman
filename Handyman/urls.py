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
from rest_framework.routers import DefaultRouter

from inventory.viewsets.invoice import InvoiceViewSet
from inventory.viewsets.order import OrderViewSet
from inventory.viewsets.product import ProductViewSet
from inventory.viewsets.vendor import VendorViewSet
from inventory.viewsets.driver import DriverViewSet

from inventory.views import register, user_login, user_logout, api_authentication, home

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('invoices', InvoiceViewSet)
router.register('orders', OrderViewSet)
router.register('vendors', VendorViewSet)
router.register('drivers', DriverViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('custom-auth/', api_authentication, name='api-auth'),
    path('home/', home, name='home'),
]