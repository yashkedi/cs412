# File: project/forms.py
# Author: Yash Kedia (yashkedi@bu.edu), 4/18/26
# Description: Forms for the Stock Screener and Backtesting Platform

from django import forms
from .models import *

class CreateStrategyForm(forms.ModelForm):
    """A form to create a new trading Strategy."""

    class Meta:
        """Associate this form with the Strategy model."""
        model = Strategy
        fields = ['name', 'description', 'indicator', 'parameter_1', 'parameter_2']

class UpdateStrategyForm(forms.ModelForm):
    """A form to update an existing trading Strategy."""

    class Meta:
        """Associate this form with the Strategy model."""
        model = Strategy
        fields = ['name', 'description', 'indicator', 'parameter_1', 'parameter_2']

class CreateScreenForm(forms.ModelForm):
    """A form to create a new stock Screen."""

    class Meta:
        """Associate this form with the Screen model."""
        model = Screen
        fields = ['name', 'sector_filter', 'min_market_cap', 'max_pe_ratio', 'min_dividend_yield']

class UpdateScreenForm(forms.ModelForm):
    """A form to update an existing stock Screen."""

    class Meta:
        """Associate this form with the Screen model."""
        model = Screen
        fields = ['name', 'sector_filter', 'min_market_cap', 'max_pe_ratio', 'min_dividend_yield']
