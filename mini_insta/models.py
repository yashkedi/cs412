# File: mini_insta/models.py
# Author: Yash Kedia (yashkedi@bu.edu), 2/12/26
# Description: Models for mini_insta application

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of an insta Profile.'''
    # define the data attributes of the Article object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.username}: {self.display_name}'
    
    def get_all_posts(self):
        '''Return a queryset of posts about this Profile.'''
        posts = Post.objects.filter(profile=self).order_by('timestamp')
        return posts
    
class Post(models.Model):
    '''Encapsulate the data of an insta Post.'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) #fk
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)
    
    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.profile} {self.caption}'
    
    def get_all_photos(self):
        '''Return a queryset of photos about this Post.'''
        photos = Photo.objects.filter(post=self)
        return photos
    
class Photo(models.Model):
    '''Encapsulate the data attributes of an image associated with a Post.'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE) #fk
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.post}'