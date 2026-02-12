# Create your views here.
# File: mini_insta/views.py
# Author: Yash Kedia (yashkedi@bu.edu), 2/12/26
# Description: Views for mini_insta application

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile
# Create your views here.

class ProfileListView(ListView):
    """View to display all profiles"""
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'
    
class ProfileDetailView(DetailView):
    '''Display a single profile.'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile" 