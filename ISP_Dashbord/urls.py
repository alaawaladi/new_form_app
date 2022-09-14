from django.urls import path
# from .views import ISP_Email
from . import views

urlpatterns = [
    #  path('home/',ISP_Email)
    path('home/',views.home),
    path('sent',views.sent),
    path('spam',views.spam),
    path('trash',views.trash),
    path('starred',views.starred),
]

