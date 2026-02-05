# File: views.py
# Author: Yash Kedia (yashkedi@bu.edu), 2/3/2026
# Description: Views for the restaurant app. Includes a main page,
# an order page with a daily special, and a confirmation page that
# processes form data and computes totals and a ready time.

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse
from datetime import datetime, timedelta
import random
import time

# Create your views here.
entree_prices = {
    "The Crispy $13": 13,
    "The Mix $15": 15,
    "The Original $14": 14,
    "The Heat $16": 16,
    "Sub Shrimp $2": 2,
}
specials = ["Miso Soup $10", "Tum Yum Soup $10", "Tom Kah Soup $10"]
special_of_the_day = specials[random.randint(0, len(specials) - 1)]

def main_page(request):
    """Display the main restaurant page."""
    template_name = "restaurant/main.html"
    context = {"time": time.ctime()}
    return render(request, template_name, context)

def order_page(request):
    '''Respond to the url 'order.html', delegate work to a template.'''
    template_name = "restaurant/order.html"

    context = {
        "time": time.ctime(),
        "special": special_of_the_day
    }

    return render(request, template_name, context)

def confirmation_page(request):
    '''Process the form submission, and generate a result.'''

    print(request.POST)

    if request.POST:

        template_name = 'restaurant/confirmation.html'

        # extract form fields into variables:
        selected_entrees = request.POST.getlist('entree')
        instructions = request.POST['instructions']
        name = request.POST['customer-name']
        phone = request.POST['customer-phone']
        email = request.POST['customer-email']

        total = 0
        for entree in selected_entrees:
            total += entree_prices[entree]

        special = request.POST.get('special')
        if special:
            total += 10
            selected_entrees.append(special_of_the_day)

        added_minutes = random.randint(30, 60)
        future_time = datetime.now() + timedelta(minutes=added_minutes)


        # create context variables for use in the template
        context = {
            "time": time.ctime(),
            'future_time': future_time,
            'selected_entrees': ', '.join(selected_entrees),
            'instructions': instructions,
            'total': total,
            'name': name,
            'phone': phone,
            'email': email
        }

        # delegate the response to the template, provide context variables
        return render(request, template_name=template_name, context=context)
    
    # default behavior: handle the GET request
    template_name = 'restaurant/order.html'


    return render(request, template_name, context)