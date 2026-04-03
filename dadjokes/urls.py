from django.urls import path
from .views import *

urlpatterns = [
    # Regular views
    path('', index),
    path('random', index),
    path('jokes', jokes),
    path('joke/<int:pk>', joke_detail),
    path('pictures', pictures),
    path('picture/<int:pk>', picture_detail),

    # REST API
    path('api/', RandomJokeAPIView.as_view()),
    path('api/random', RandomJokeAPIView.as_view()),
    path('api/jokes', JokeListAPIView.as_view()),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view()),
    path('api/pictures', PictureListAPIView.as_view()),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view()),
    path('api/random_picture', RandomPictureAPIView.as_view()),
]
