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


    def get_followers(self):
        '''return all followers of a given profile'''
        followers = Follow.objects.filter(profile=self)
        return [f.follower_profile for f in followers]
    
    def get_num_followers(self):
        '''return the number of followers a given profile has'''
        follower_list = self.get_followers()
        return len(follower_list)
    
    def get_following(self):
        '''return the profiles that a given profile follows'''
        following = Follow.objects.filter(follower_profile=self)
        return [f.profile for f in following]
    
    def get_num_following(self):
        '''return the number of following a given profile has'''
        following_list = self.get_following()
        return len(following_list)
    
    def get_post_feed(self):
        '''return a list of posts specifically for the profiles being followed by a given profile'''
        following = self.get_following()
        return Post.objects.filter(profile__in=following).order_by('-timestamp') 
    
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

    def get_first_photo(self):
        '''Return the first photo of this Post or None if no photo.'''
        photos = Photo.objects.filter(post=self).first()
        return photos
    
    def get_all_comments(self):
        '''Return all comments of a given post'''
        comments = Comment.objects.filter(post=self)
        return comments
    
    def get_likes(self):
        '''Return all likes for a given post'''
        likes = Like.objects.filter(post=self)
        return likes
    
    '''Adding these 2 functions to make it look like the professors example'''
    
    def get_first_like(self):
        '''Return the first like profile of this Post or None if no likes.'''
        like = Like.objects.filter(post=self).first()
        return like
    
    def get_num_likes(self):
        '''Return the number of likes of this Post'''
        likes = Like.objects.filter(post=self).count()
        return (likes - 1)
    
class Photo(models.Model):
    '''Encapsulate the data attributes of an image associated with a Post.'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE) #fk
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.post}'
        
    def get_image_url(self):
        '''an accessor method, return the URL to the image'''
        if self.image_url:
            return self.image_url
        else:
            return self.image_file.url
        
class Follow(models.Model):
    '''Encapsulate the data attributes of a Follow relationship.'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile") #profile that's being followed
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile") #profile that does the following
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.follower_profile} follows {self.profile}'
    
class Comment(models.Model):
    '''Encapsulate the data attributes of a comment on a post.'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.text}'
    
class Like(models.Model):
    '''Encapsulate the data attributes of a like on a post'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.profile} liked {self.post}'