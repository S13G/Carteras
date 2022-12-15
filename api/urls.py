from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from api import views


urlpatterns = [
    # JWT URLS
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.get_routes),
    path('projects/', views.get_projects),
    path('project/<str:pk>/', views.get_project),
    path('project/<str:pk>/vote/', views.project_vote),
]