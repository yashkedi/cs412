# File: views.py
# Author: Yash Kedia (yashkedi@bu.edu), 1/27/2026
# Description: Django views for the quotes app. Displays a random

from django.shortcuts import render
from django.http import HttpResponse
import random
import time

steve_jobs_quotes= [
    "Stay hungry, stay foolish.",
    "Your time is limited, so don’t waste it living someone else’s life.",
    "Sometimes life hits you in the head with a brick. Don’t lose faith."
]
steve_jobs_img=[
    "https://static.wikia.nocookie.net/ipod/images/c/cb/Jobs_hero20110329.png/revision/latest?cb=20200202110213",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Steve_Jobs_Headshot_2010-CROP_%28cropped_2%29.jpg/500px-Steve_Jobs_Headshot_2010-CROP_%28cropped_2%29.jpg",
    "https://image.cnbcfm.com/api/v1/image/100496736-steve-jobs-march-2011-getty.jpg?v=1617291443&w=1480&h=833&ffmt=webp&vtcrop=y"

]

def quote_page(request):
    '''Respond to the url 'quote.html', delegate work to a template.'''
    template_name = 'quotes/quote.html'
    context = {
        "quote": steve_jobs_quotes[random.randint(0, len(steve_jobs_quotes) - 1)],
        "image": steve_jobs_img[random.randint(0, len(steve_jobs_img) - 1)],
        "time": time.ctime()
    }
    return render(request, template_name, context)

def show_all_page(request):
    '''Respond to the url 'show_all.html', delegate work to a template.'''
    template_name = 'quotes/show_all.html'
    context = {
        "quotes": steve_jobs_quotes,
        "images": steve_jobs_img,
        "time": time.ctime()
    }
    return render(request, template_name, context)

def about_page(request):
    '''Respond to the url 'about_page.html', delegate work to a template.'''
    template_name = 'quotes/about.html'
    context = {
        "time": time.ctime()
    }
    return render(request, template_name, context)
    