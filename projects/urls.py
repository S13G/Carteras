from django.urls import path
from . import views


urlpatterns = [
    path('projects/', views.projects, name='projects'),
    path('projects/<str:pk>/', views.project, name='project'),
]