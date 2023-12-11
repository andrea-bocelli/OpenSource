from django.urls import path
from .views import *

urlpatterns = [
    path('', StationView.as_view()),
]