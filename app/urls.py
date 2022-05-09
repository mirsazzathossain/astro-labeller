from os import name
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='home'),
    path('galaxy/get_started', views.get_started, name='get_started'),
    path('galaxies/<str:galaxy_name>/', views.galaxy, name='galaxy'),
    path('galaxies/<str:galaxy_name>/next', views.galaxy_next, name='galaxy_next'),
    path('galaxies/<str:galaxy_name>/prev', views.galaxy_prev, name='galaxy_prev'),
]