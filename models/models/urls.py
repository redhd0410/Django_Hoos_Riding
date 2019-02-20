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

    #MANY###########################################
    path('api/rides/n/<int:n>/date/<str:date>/<int:is_after>',views.getNSoonestRides),
    path('api/user/id/<int:pk>/rides/<int:n>/date/<str:date>/<int:is_after>', views.getNUserRideHistory),
    path('api/user/driver/id/<int:pk>/rides/<int:n>/date/<str:date>/<int:is_after>', views.getDriverRideHistory),
    #SINGLE#########################################
    
    # Post
    path('api/user', views.user),
    # Update/Delete/Get a User
    path('api/user/id/<int:pk>', views.user),


    # Post
    path('api/vehicle', views.vehicle),
    # Update/Delete/Get Vehicle
    path('api/vehicle/id/<int:pk>', views.vehicle),


    # Post
    path('api/ride', views.ride),
    #Get/Delete Single Ride
    path('api/ride/id/<int:pk>', views.ride),
    # Update Ride with passenger
    path('api/ride/id/<int:pk>/pid/<int:uid>', views.ride),

]
