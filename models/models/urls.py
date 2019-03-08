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
    #AUTHENTICATOR#########################################
    path('api/authenticator/<int:user_id>', views.createAuthenticator), #Returns authenticator
    path('api/checkcookie/<str:auth_str>', views.isAuthTokenValid),
    
    
    #MANY###########################################
    path('api/rides/n/<int:n>/date/<str:date>/<int:is_after>',views.getNSoonestRides, name = "getNSoonestRides"),
    path('api/user/id/<int:pk>/rides/<int:n>/date/<str:date>/<int:is_after>', views.getNUserRideHistory, name = "getNUserRideHistory"),
    path('api/user/driver/id/<int:pk>/rides/<int:n>/date/<str:date>/<int:is_after>', views.getDriverRideHistory, name = "getDriverRideHistory"),
    
    
    #SINGLE#########################################
    # Post & Get Many User
    path('api/users', views.user, name = "user_result"),
    # Update/Delete/Get a User
    path('api/users/<int:pk>', views.user, name = "user_result_id"),


    # Post & Get Many Vehicle
    path('api/vehicles', views.vehicle, name = "vehicle_result"),
    path('api/vehicles/all', views.getAllVehicles, name = "getAllVehicles"),
    # Update Vehicle & Get Vehicle
    path('api/vehicles/<int:pk>', views.vehicle, name = "vehicle_result_id"),


    # Post & Get Many Rides
    path('api/rides', views.ride, name = "ride_result"),
    #Get/Delete Single Ride
    path('api/rides/<int:pk>', views.ride, name = "ride_result_id"),
    # Update Ride
    path('api/rides/<int:pk>/<int:uid>', views.ride, name = "ride_result_uid"),

]
