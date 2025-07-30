from django.contrib import admin
from django.urls import path
from event.views import Home
urlpatterns = [
    path('home/', Home)
]
