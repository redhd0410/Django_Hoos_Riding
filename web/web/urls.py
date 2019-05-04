from django.contrib import admin
from django.urls import path
from web import views
import django.views.static




urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.homepage),
    path('ridedetails/<int:pk>', views.ridedetails),
    path('createaccount/', views.createaccount, name="createaccount"),
    path('login/', views.login, name="login"),
    path('createlisting/', views.createListing, name="createlisting"), 
    path('logout/', views.LogOut, name="logout"),
    path('search/', views.search, name="search"),
]

#urlpatterns += [   url(r'^static/(?P>path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG})]
