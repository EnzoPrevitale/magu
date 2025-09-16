from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path("pagantes/", pagante_list),
    path("pagantes/<int:pk>", pagante_detail),
]