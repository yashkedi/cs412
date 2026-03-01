# File: mini_insta/forms.py
# Author: Yash Kedia (yashkedi@bu.edu), 2/19/2026
# Description: forms for mini_insta application

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add a post to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Post
        fields = ['caption']
        
class UpdateProfileForm(forms.ModelForm):
    '''A form to update a profile in the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']
        
class UpdatePostForm(forms.ModelForm):
    '''A form to update a post in the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Post
        fields = ['caption']