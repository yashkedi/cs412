# File: mini_insta/serializers.py
# Author: Yash Kedia (yashkedi@bu.edu)
# Description: DRF serializers for mini_insta REST API

from rest_framework import serializers
from .models import Profile, Post, Photo


class PhotoSerializer(serializers.ModelSerializer):
    '''Serializer for Photo objects. Adds a computed image field that returns
    the best available URL (image_url takes priority over uploaded image_file).'''

    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image_url', 'image_file', 'timestamp', 'image']

    def get_image(self, obj):
        '''Return the resolved image URL, building an absolute URI for uploaded files.'''
        if obj.image_url:
            return obj.image_url
        try:
            if obj.image_file:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.image_file.url)
                return obj.image_file.url
        except ValueError:
            pass
        return None


class PostSerializer(serializers.ModelSerializer):
    '''Serializer for Post objects. Includes a nested list of photos via
    a computed field so each post response contains its full photo data.'''

    photos = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'profile', 'timestamp', 'caption', 'photos']

    def get_photos(self, obj):
        '''Return serialized photos for this post, passing request context
        through so PhotoSerializer can build absolute image URLs.'''
        photos = obj.get_all_photos()
        return PhotoSerializer(photos, many=True, context=self.context).data


class PostCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating a new Post. Only exposes the caption field;
    the profile is set in the view from the URL kwargs.'''

    class Meta:
        model = Post
        fields = ['caption']


class ProfileSerializer(serializers.ModelSerializer):
    '''Serializer for Profile objects. Exposes public-facing profile fields
    used by the list and detail API endpoints.'''

    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text', 'join_date']
