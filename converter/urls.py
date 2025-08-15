from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download_video/', views.download_video, name='download_video'),
    path('download_audio/', views.download_audio, name='download_audio'),
    path('download/<str:filename>/', views.download_file, name='download_file'),
]
