from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('experience/login/', views.Login),
    path('experience/createaccount', views.createAccount),
    
    path('admin/', admin.site.urls),
    path('experience/homepage/get/<str:auth>', views.getHomePage),
    path('experience/detailpage/get/<int:pk>/<str:auth>', views.getDetailPage),
    path('experience/createlisting/<str:auth>', views.createListing)
]

 #path('experience/homepage/update/<int:user_id>/<int:ride_id>', views.UpdateRide),
 #path('experience/homepage/remove/<int:user_id>/<int:ride_id>', views.RemoveSelfRide),
