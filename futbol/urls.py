from django.urls import path
from . import views

urlpatterns = [
    path('', views.classificacio, name='classificacio'),
]