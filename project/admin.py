# File: project/admin.py
# Author: Yash Kedia (yashkedi@bu.edu), 4/18/26
# Description: Admin registration for the Stock Screener and Backtesting Platform

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Stock)
admin.site.register(Investor)
admin.site.register(Screen)
admin.site.register(Strategy)
admin.site.register(BacktestResult)
