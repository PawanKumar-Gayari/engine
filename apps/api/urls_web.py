from django.urls import path
from .views import generate_page

urlpatterns = [
    path('', generate_page, name="generate_page"),
]