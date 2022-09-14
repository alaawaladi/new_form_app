from django.contrib import admin
from django.urls import path,include
from ISP_accounts import views
from ISP_Dashbord import views

urlpatterns = [
    path('',include('ISP_accounts.urls')),
    
    path('home/',views.home,name="home"),
    
    path('sent/',views.sent,name="sent"),
    
    path('spam/',views.spam,name="spam"),
    
    path('trash/',views.trash,name="trash"),
    
    path('starred/',views.starred,name="starred"),
    
    path('admin/', admin.site.urls),
]
