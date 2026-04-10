# Create your views here.
# File: mini_insta/views.py
# Author: Yash Kedia (yashkedi@bu.edu), 2/12/26
# Description: Views for mini_insta application

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from mini_insta.forms import *
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import ProfileSerializer, PostSerializer, PostCreateSerializer
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
    

class PostDetailView(DetailView):
    '''Display a single post.'''

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post" 

    def get_context_data(self, **kwargs):
        '''Override get_context_data to add profile to context for footer.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['profile'] = Profile.objects.filter(user=self.request.user).first()
        return context

class CreatePostView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Post.
    (1) Display the html form to the user (GET)
    (2) Process form submission and store the new post object (POST)
    '''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def get_context_data(self, **kwargs):
        '''override the built in get_context_data to populate fields.'''
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(user=self.request.user)
        return context
    
    def form_valid(self, form):
        '''validate incoming create post form'''
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile
        image_file = self.request.FILES.getlist('files')
        post = form.save()
        if image_file:
            for file in image_file:
                Photo.objects.create(post=post, image_file=file)
        return super().form_valid(form)
        
        
    def get_success_url(self):
        '''redirect to the new Post’s detail page'''
        return reverse("show_post", kwargs={"pk": self.object.pk})
    

    def get_object(self):
        '''return one instance of the Profile object.'''
        return Profile.objects.get(user=self.request.user)
    
    def get_login_url(self):
        '''return the url for this app's login page'''
        return reverse('login')

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''a view to handle the update of a profile.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def get_success_url(self):
        # redirect to the updated profile page
        return reverse("show_my_profile")
    
    def get_login_url(self):
        '''return the url for this app's login page'''
        return reverse('login')
    
class DeletePostView(LoginRequiredMixin, DeleteView):
    '''a view to handle the deletion of a post.'''
    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self,  **kwargs):
        '''override the built in get_context_data to populate fields.'''
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        profile = post.profile
        context['post'] = post
        context['profile'] = profile
        return context
    
    def get_success_url(self):
        '''redirect to the deleted post's corresponding profile detail page.'''
        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})
    
class UpdatePostView(LoginRequiredMixin, UpdateView):
    '''a view to handle updating a post.'''
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_context_data(self,  **kwargs):
        '''override the built in get_context_data to populate fields.'''
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        profile = post.profile
        caption = post.caption
        context['post'] = post
        context['caption'] = caption
        context['profile'] = profile
        return context
    
    def get_success_url(self):
        '''redirect to the updated post's detail page.'''
        return reverse("show_post", kwargs={"pk": self.object.pk})
class ShowFollowersDetailView(DetailView):
    '''a view to handle displaying followers'''
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

    def get_context_data(self,  **kwargs):
        '''override the built in get_context_data to populate fields.'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['followers'] = profile.get_followers()
        context['num_followers'] = profile.get_num_followers()
        return context
    
class ShowFollowingDetailView(DetailView):
    '''a view to handle displaying following'''
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

    def get_context_data(self,  **kwargs):
        '''override the built in get_context_data to populate fields.'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["following"] = profile.get_following()
        context["num_following"] = profile.get_num_following()
        return context

class PostFeedListView(LoginRequiredMixin, ListView):
    '''A view to handle displaying the post feed of a given profile.'''
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        '''Return the posts in the feed for this profile.'''
        profile = Profile.objects.get(user=self.request.user)
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        '''Add the current profile to the context.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context
    
    def get_login_url(self):
        '''return the url for this app's login page'''
        return reverse('login')
    
class SearchView(LoginRequiredMixin, ListView):
    '''a view to handle searching for profiles and posts'''
    model = Profile
    template_name = "mini_insta/search_results.html"
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        '''if no query render template form, otherwise return dispatch'''
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if "q" not in self.request.GET:
            profile = Profile.objects.get(user=self.request.user)
            return render(request, "mini_insta/search.html", {"profile": profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''return posts which match the query'''
        query = self.request.GET.get("q")
        if query:
            return Post.objects.filter(caption__icontains=query)
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        '''add profile, query, posts, and matching profiles to context'''
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        profile = Profile.objects.get(user=self.request.user)
        posts = self.get_queryset()
        matching_profiles = Profile.objects.filter(username__icontains=query) | \
                            Profile.objects.filter(display_name__icontains=query) | \
                            Profile.objects.filter(bio_text__icontains=query)
        context["profile"] = profile
        context["query"] = query
        context["posts"] = posts
        context["profiles"] = matching_profiles
        return context


    def get_login_url(self):
        '''return the url for this app's login page'''
        return reverse('login')
    
class MyProfileDetailView(LoginRequiredMixin, DetailView):
    '''Display the logged-in user's own profile.'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        '''Return the profile of the logged-in user.'''
        return Profile.objects.get(user=self.request.user)
    
class CreateProfileView(CreateView):
    '''A view for handling creating a profile.'''
    model = Profile
    template_name = "mini_insta/create_profile_form.html"
    fields = ['username', 'display_name', 'profile_image_url', 'bio_text']

    def get_context_data(self, **kwargs):
        ''''override the built in get_context_data to populate fields.'''
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''validate incoming create profile form'''
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
            return super().form_valid(form)
        else:
            context = self.get_context_data(form=form)
            context['user_form'] = user_form
            return self.render_to_response(context)
    
    def get_success_url(self):
        '''redirect to the Profile's detail page'''
        return reverse('show_my_profile')
    
class CreateFollowView(LoginRequiredMixin, CreateView):
    '''A view for handling a profile following another profile.'''
    model = Follow
    form_class = CreateFollowForm
    template_name = "mini_insta/follow_form.html"

    def get_login_url(self):
        '''Return the url for this app's login page.'''
        return reverse('login')

    def get_context_data(self, **kwargs):
        '''Override the built in get_context_data to populate fields.'''
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs["pk"])
        context["follower_profile"] = Profile.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        '''Set the follower and followed profiles before saving.'''
        form.instance.profile = Profile.objects.get(pk=self.kwargs["pk"])
        form.instance.follower_profile = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect to the followed profile's detail page.'''
        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})


class DeleteFollowView(LoginRequiredMixin, DeleteView):
    '''A view to handle the deletion of a follow relationship.'''
    model = Follow
    template_name = "mini_insta/delete_follow_form.html"
    form_class = DeleteFollowForm

    def get_login_url(self):
        '''Return the url for this app's login page.'''
        return reverse('login')

    def get_object(self, queryset=None):
        '''Return the follow object between the current user and target profile.'''
        profile_to_unfollow = Profile.objects.get(pk=self.kwargs["pk"])
        follower_profile = Profile.objects.get(user=self.request.user)
        return Follow.objects.get(profile=profile_to_unfollow, follower_profile=follower_profile)

    def get_context_data(self, **kwargs):
        '''Override the built in get_context_data to populate fields.'''
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs["pk"])
        context["follower_profile"] = Profile.objects.get(user=self.request.user)
        return context

    def get_success_url(self):
        '''Redirect to the unfollowed profile's detail page.'''
        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})


class LikeDetailView(LoginRequiredMixin, CreateView):
    '''A view to handle liking a post.'''
    model = Like

    def get_login_url(self):
        '''Return the url for this app's login page.'''
        return reverse('login')

    def post(self, request, *args, **kwargs):
        '''Create a like object if the user is not liking their own post.'''
        post = Post.objects.get(pk=self.kwargs["pk"])
        profile = Profile.objects.get(user=request.user)
        if post.profile != profile:
            Like.objects.get_or_create(post=post, profile=profile)
        return redirect("show_post", pk=post.pk)


class LikeDeleteView(LoginRequiredMixin, DeleteView):
    '''A view to handle unliking a post.'''
    model = Like

    def get_login_url(self):
        '''Return the url for this app's login page.'''
        return reverse('login')

    def post(self, request, *args, **kwargs):
        '''Delete the like object if it exists.'''
        post = Post.objects.get(pk=self.kwargs["pk"])
        profile = Profile.objects.get(user=request.user)
        like = Like.objects.filter(post=post, profile=profile).first()
        if like:
            like.delete()
        return redirect("show_post", pk=post.pk)


class LoginAPIView(APIView):
    '''POST /api/login/ — authenticate with username+password, return token + profile_id.
    Open to unauthenticated users so the login screen can reach it.'''

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            request,
            username=request.data.get('username'),
            password=request.data.get('password'),
        )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            profile = Profile.objects.filter(user=user).first()
            return Response({
                'token': token.key,
                'user': {'id': user.id, 'username': user.username},
                'profile_id': profile.id if profile else None,
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileListAPIView(APIView):
    '''GET /api/profiles/ — list all profiles (read-only for unauthenticated).'''

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class ProfileDetailAPIView(APIView):
    '''GET /api/profiles/<pk>/ — single profile detail.'''

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ProfilePostsAPIView(APIView):
    '''GET /api/profiles/<pk>/posts/ — all posts + photos for a profile. Requires auth.'''

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        posts = profile.get_all_posts()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileFeedAPIView(APIView):
    '''GET /api/profiles/<pk>/feed/ — feed of posts from followed profiles. Requires auth.'''

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        posts = profile.get_post_feed()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class CreatePostAPIView(APIView):
    '''POST /api/profiles/<pk>/create_post/ — create a new post. Requires auth.'''

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
