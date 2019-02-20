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
    # Post & Get Many User
    path('api/users', views.user, name = "user_result"),
    # Update/Delete/Get a User
    path('api/users/<int:pk>', views.user, name = "user_result_id"),


    # Post & Get Many Vehicle
    path('api/vehicles', views.vehicle, name = "vehicle_result"),
    # Update Vehicle & Get Vehicle
    path('api/vehicles/<int:pk>', views.vehicle, name = "vehicle_result_id"),


    # Post & Get Many Rides
    path('api/rides', views.ride, name = "rides_result"),
    #Get/Delete Single Ride
    path('api/rides/<int:pk>', views.ride, name = "rides_result_id"),
    # Update Ride
    path('api/rides/<int:pk>/<int:uid>', views.ride, name = "rides_result_uid"),

]
