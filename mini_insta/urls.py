# File: mini_insta/urls.py
# Author: Yash Kedia (yashkedi@bu.edu), 2/12/26
# Description: Urls for mini_insta application

from django.urls import path
from .views import *

urlpatterns = [
    path(r'', ProfileListView.as_view(), name="show_all_profiles"),
    path(r'show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
]