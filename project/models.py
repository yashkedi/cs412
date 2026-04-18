# File: project/models.py
# Author: Yash Kedia (yashkedi@bu.edu), 4/18/26
# Description: Models for the Quantitative Stock Screener and Backtesting Platform

from django.db import models
from django.urls import reverse

class Stock(models.Model):
    '''Encapsulate the data of a single stock in the universe.'''

    ticker = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100)
    exchange = models.CharField(max_length=50)
    market_cap = models.FloatField()
    pe_ratio = models.FloatField(null=True, blank=True)
    dividend_yield = models.FloatField(null=True, blank=True)
    beta = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        '''Return a string representation of this Stock.'''
        return f'{self.ticker}: {self.company_name}'

    def get_absolute_url(self):
        '''Return the URL to display this Stock's detail page.'''
        return reverse('stock_detail', kwargs={'ticker': self.ticker})


class Investor(models.Model):
    '''Encapsulate the data of an Investor on the platform.'''

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this Investor.'''
        return f'{self.username}: {self.first_name} {self.last_name}'

    def get_strategies(self):
        '''Return all strategies belonging to this investor.'''
        return Strategy.objects.filter(investor=self)

    def get_screens(self):
        '''Return all screens belonging to this investor.'''
        return Screen.objects.filter(investor=self)

    def get_absolute_url(self):
        '''Return the URL to display this Investor's dashboard.'''
        return reverse('investor_dashboard', kwargs={'pk': self.pk})


# Choices for the strategy indicator field
INDICATOR_CHOICES = [
    ('SMA_CROSSOVER', 'SMA Crossover'),
    ('RSI', 'RSI'),
    ('MOMENTUM', 'Momentum'),
]

class Screen(models.Model):
    '''Encapsulate the data of a stock screening filter set owned by an investor.'''

    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    sector_filter = models.CharField(max_length=100, blank=True)
    min_market_cap = models.FloatField(null=True, blank=True)
    max_pe_ratio = models.FloatField(null=True, blank=True)
    min_dividend_yield = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this Screen.'''
        return f'{self.name} ({self.investor.username})'

    def run(self):
        '''Apply this screen's filters to the Stock universe and return matching stocks.'''
        results = Stock.objects.all()
        if self.sector_filter:
            results = results.filter(sector=self.sector_filter)
        if self.min_market_cap is not None:
            results = results.filter(market_cap__gte=self.min_market_cap)
        if self.max_pe_ratio is not None:
            results = results.filter(pe_ratio__lte=self.max_pe_ratio)
        if self.min_dividend_yield is not None:
            results = results.filter(dividend_yield__gte=self.min_dividend_yield)
        return results

    def get_absolute_url(self):
        '''Return the URL to run this screen.'''
        return reverse('run_screener', kwargs={'pk': self.pk})


class Strategy(models.Model):
    '''Encapsulate the data of a trading strategy owned by an investor.'''

    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    indicator = models.CharField(max_length=20, choices=INDICATOR_CHOICES)
    parameter_1 = models.FloatField()   # short window (SMA), RSI period, or lookback
    parameter_2 = models.FloatField(null=True, blank=True)  # long window (SMA only)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this Strategy.'''
        return f'{self.name} ({self.get_indicator_display()})'

    def get_backtests(self):
        '''Return all backtest results for this strategy, newest first.'''
        return BacktestResult.objects.filter(strategy=self).order_by('-ran_on')

    def get_absolute_url(self):
        '''Return the URL to display this Strategy's detail page.'''
        return reverse('strategy_detail', kwargs={'pk': self.pk})


class BacktestResult(models.Model):
    '''Encapsulate the performance metrics from running a strategy against a stock.'''

    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_return = models.FloatField()    # percentage
    max_drawdown = models.FloatField()   # percentage (negative)
    win_rate = models.FloatField()       # percentage of winning trades
    num_trades = models.IntegerField()   # number of round-trip trades
    ran_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this BacktestResult.'''
        return f'{self.strategy.name} on {self.stock.ticker} ({self.start_date} to {self.end_date})'

    def get_absolute_url(self):
        '''Return the URL to display this BacktestResult's detail page.'''
        return reverse('backtest_result', kwargs={'pk': self.pk})
