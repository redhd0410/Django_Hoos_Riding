from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    #
    #
    #AUTHENTICATOR
    #
    #

    path('api/authenticator/<int:user_id>', views.createAuthenticator, name="createauthenticator"), #Returns authenticator
    path('api/checkcookie/<str:auth_str>', views.isAuthTokenValid, name="checkcookie"),
    path('api/auth/users/<str:auth_str>', views.getUserIdFromAuth),
    path('api/auth/vehicles/<str:auth_str>', views.getVehicleIdFromAuth),
    
    
    #
    #
    # MANY (PRIMARY HOME PAGE)
    #
    #

    path('api/rides/n/<int:n>/date/<str:date>/<int:is_after>',views.getNSoonestRides, name = "getNSoonestRides"),
    path('api/user/id/<int:pk>/rides/<int:n>/date/<str:date>/<int:is_after>', views.getNUserRideHistory, name = "getNUserRideHistory"),
    path('api/user/driver/id/<int:pk>/rides/<int:n>/date/<str:date>/<int:is_after>', views.getDriverRideHistory, name = "getDriverRideHistory"),
    


    #
    #
    # SINGLE (GET/PUT/POST/DELETE)
    #
    #

    path('api/users/<int:pk>', views.user, name = "user_result_id"),
    path('api/vehicles/<int:pk>', views.vehicle, name = "vehicle_result_id"),
    path('api/rides/<int:pk>', views.ride, name = "ride_result_id"),


    #
    #
    # UPDATE RIDE
    #
    #

    path('api/rides_update/<int:pk>/<int:uid>', views.ride, name = "ride_result_uid"),

]
