from django.urls import path
from .import views

urlpatterns = [
     path('',views.index),
     path('hello/', views.HelloView.as_view(), name='hello'),
]
