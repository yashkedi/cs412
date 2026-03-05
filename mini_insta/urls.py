# File: mini_insta/urls.py
# Author: Yash Kedia (yashkedi@bu.edu), 2/12/26
# Description: Urls for mini_insta application

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404

urlpatterns = [
    path(r'', ProfileListView.as_view(), name="show_all_profiles"),
    path(r'show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='show_post'),
    path(r'post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path(r'post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path(r'profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
    path(r'profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),
    path(r'profile/', MyProfileDetailView.as_view(), name='show_my_profile'),
    path(r'profile/create_post', CreatePostView.as_view(), name="create_post"),
    path(r'profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path(r'profile/feed', PostFeedListView.as_view(), name="show_feed"),
    path(r'profile/search', SearchView.as_view(), name="show_search"),
    path('login/', auth_views.LoginView.as_view(template_name="mini_insta/login.html"), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name="logout"),
    path(r'logout_confirmation/', TemplateView.as_view(template_name='mini_insta/logged_out.html'), name="logout_confirmation"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/follow', CreateFollowView.as_view(), name="follow_profile"),
    path('profile/<int:pk>/delete_follow', DeleteFollowView.as_view(), name="delete_follow"),
    path('post/<int:pk>/like', LikeDetailView.as_view(), name="like_post"),
    path('post/<int:pk>/delete_like', LikeDeleteView.as_view(), name="delete_like"),
]