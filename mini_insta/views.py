# Create your views here.
# File: mini_insta/views.py
# Author: Yash Kedia (yashkedi@bu.edu), 2/12/26
# Description: Views for mini_insta application

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from mini_insta.forms import *
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

class CreatePostView(CreateView):
    '''A view to handle creation of a new Post.
    (1) Display the html form to the user (GET)
    (2) Process form submission and store the new post object (POST)
    '''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def get_context_data(self, **kwargs):
        '''override the built in get_context_data to populate fields.'''
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        '''validate incoming create post form'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
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

class UpdateProfileView(UpdateView):
    '''a view to handle the update of a profile.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    
    def get_success_url(self):
        # redirect to the updated profile page
        return reverse("show_profile", kwargs={"pk": self.object.pk})
    
class DeletePostView(DeleteView):
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
    
class UpdatePostView(UpdateView):
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

class PostFeedListView(ListView):
    '''A view to handle displaying the post feed of a given profile.'''
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        '''Return the posts in the feed for this profile.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        '''Add the current profile to the context.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context
    
class SearchView(ListView):
    '''a view to handle searching for profiles and posts'''
    model = Profile
    template_name = "mini_insta/search_results.html"
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        '''if no query render template form, otherwise return dispatch'''
        if "q" not in self.request.GET:
            profile = Profile.objects.get(pk=self.kwargs['pk'])
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
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        posts = self.get_queryset()
        matching_profiles = Profile.objects.filter(username__icontains=query) | \
                            Profile.objects.filter(display_name__icontains=query) | \
                            Profile.objects.filter(bio_text__icontains=query)
        context["profile"] = profile
        context["query"] = query
        context["posts"] = posts
        context["profiles"] = matching_profiles
        return context