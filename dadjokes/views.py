import random
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer


# --- Regular Django views ---

def index(request):
    joke = random.choice(Joke.objects.all()) if Joke.objects.exists() else None
    picture = random.choice(Picture.objects.all()) if Picture.objects.exists() else None
    return render(request, 'dadjokes/index.html', {'joke': joke, 'picture': picture})

def jokes(request):
    return render(request, 'dadjokes/jokes.html', {'jokes': Joke.objects.all()})

def joke_detail(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    return render(request, 'dadjokes/joke_detail.html', {'joke': joke})

def pictures(request):
    return render(request, 'dadjokes/pictures.html', {'pictures': Picture.objects.all()})

def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, 'dadjokes/picture_detail.html', {'picture': picture})


# --- REST API views ---

class RandomJokeAPIView(APIView):
    def get(self, request):
        joke = random.choice(Joke.objects.all()) if Joke.objects.exists() else None
        if joke is None:
            return Response({'error': 'No jokes available'}, status=404)
        serializer = JokeSerializer(joke)
        return Response(serializer.data)

class JokeListAPIView(generics.ListCreateAPIView):
    queryset = Joke.objects.order_by('id')
    serializer_class = JokeSerializer
    pagination_class = None

class JokeDetailAPIView(generics.RetrieveAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListAPIView):
    queryset = Picture.objects.order_by('id')
    serializer_class = PictureSerializer
    pagination_class = None

class PictureDetailAPIView(generics.RetrieveAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomPictureAPIView(APIView):
    def get(self, request):
        picture = random.choice(Picture.objects.all()) if Picture.objects.exists() else None
        if picture is None:
            return Response({'error': 'No pictures available'}, status=404)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)
