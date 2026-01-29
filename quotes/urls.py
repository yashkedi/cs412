# File: urls.py
# Author: Yash Kedia (yashkedi@bu.edu), 1/27/2026
# Description: URL patterns for the quotes app.

from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path(r'', views.quote_page, name='quote_page'),
    path(r'quote', views.quote_page, name='quote_page'),
    path(r'show_all', views.show_all_page, name='show_all_page'),
    path(r'about', views.about_page, name='about_page')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)