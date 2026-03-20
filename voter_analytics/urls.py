# voter_analytics/urls.py
# Yash Kedia (yashkedi@bu.edu), 3/19/26
# URL patterns for voter_analytics app

from django.urls import path
from . import views

urlpatterns = [
    path('', views.VotersListView.as_view(), name='voters'),                  # paginated voter list with filters
    path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),   # detail page for a single voter by primary key
    path('graphs', views.GraphListView.as_view(), name='graphs'),             # analytics graphs page with same filter controls
]