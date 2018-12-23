from django.urls import path
from django.contrib import admin
from . import views

app_name = 'albumApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('upurl/', views.upUrl, name='upUrl'),
    path('search/', views.search, name='search'),
    path('jq/',views.jq ,name='jq')
]