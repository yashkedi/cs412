# File: mini_insta/urls.py
# Author: Yash Kedia (yashkedi@bu.edu), 2/12/26
# Description: Urls for mini_insta application

from django.urls import path
from .views import *

urlpatterns = [
    path(r'', ProfileListView.as_view(), name="show_all_profiles"),
    path(r'show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='show_post'),
    path(r'profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
    path(r'profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path(r'post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path(r'post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path(r'profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
    path(r'profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),
    path(r'profile/<int:pk>/feed', PostFeedListView.as_view(), name="show_feed"),
    path(r'profile/<int:pk>/search', SearchView.as_view(), name="show_search"),
]