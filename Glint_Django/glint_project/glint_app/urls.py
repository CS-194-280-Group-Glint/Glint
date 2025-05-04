from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('podcast/', views.podcast, name='podcast'),
    path('api/save_preferences/', views.save_preferences, name='save_preferences'),
]