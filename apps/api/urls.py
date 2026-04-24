from django.urls import path
from .views import generate_post

urlpatterns = [
    path('generate/', generate_post),
]