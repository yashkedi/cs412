# File: urls.py
# Author: Yash Kedia (yashkedi@bu.edu), 2/3/2026
# Description: URL patterns for the restaurant app.

from django.urls import path
from . import views

urlpatterns = [
    path(r"", views.main_page, name="main_page"),
    path(r"main", views.main_page, name="main_page"),
    path(r"order", views.order_page, name="order_page"),
    path(r"confirmation", views.confirmation_page, name="confirmation_page"),
]