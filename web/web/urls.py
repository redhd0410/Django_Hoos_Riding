from django.contrib import admin
from django.urls import path
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.homepage),
    path('ridedetails/<int:pk>', views.ridedetails),
    path('createaccount/', views.createaccount, name="createaccount"),
    path('login/', views.login, name="login"),
    path('createlisting/', views.createListing, name="createlisting"), 
    path('logout/', views.LogOut, name="logout"),
]
