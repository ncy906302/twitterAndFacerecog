from django.urls import path
from django.contrib import admin
from . import views

app_name = 'faceRecog'

urlpatterns = [
    path('', views.match, name='match'),
    path('recog/', views.recog, name='recog'),
]