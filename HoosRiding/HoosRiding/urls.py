"""HoosRiding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),

    # Post & Get User
    path('api/users', views.user),
    path('api/users/<int:pk>', views.user),
    path('api/users/<int:pk>/update'),
    path('api/users/<int:pk>/delete'),
    path('api/users/create'),

    # Post & Get Vehicle
    path('api/vehicles', views.vehicle),
    path('api/vehicles/<int:pk>', views.vehicle),
    path('api/vehicles/<int:pk>/update'),
    path('api/vehicles/<int:pk>/delete'),
    path('api/vehicles/create'),

    # Post & Get Rides
    path('api/rides', views.ride),
    path('api/rides/<int:pk>', views.ride),
    path('api/rides/<int:pk>/update', views.ride),
    path('api/rides/<int:pk>/delete', views.ride),
    path('api/rides/create', views.ride),

    path('admin/', admin.site.urls),
]
