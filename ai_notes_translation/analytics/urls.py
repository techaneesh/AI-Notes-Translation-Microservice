from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.stats_view, name='stats'),
    path('cache-info/', views.cache_info_view, name='cache-info'),
]

