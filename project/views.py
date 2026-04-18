# File: project/views.py
# Author: Yash Kedia (yashkedi@bu.edu), 4/18/26
# Description: Views for the Quantitative Stock Screener and Backtesting Platform

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import *
from .forms import *

def _run_backtest_engine(strategy, stock, start_date, end_date):
    '''Fetch historical price data from Yahoo Finance and simulate the given strategy. Returns a metrics dict or None.'''
    import yfinance as yf
    import pandas as pd

    df = yf.download(stock.ticker, start=str(start_date), end=str(end_date), progress=False)
    if df.empty:
        return None

    prices = df['Close'].squeeze()
    p1 = float(strategy.parameter_1)
    p2 = float(strategy.parameter_2) if strategy.parameter_2 is not None else None

    # Generate signal: 1 = in market, 0 = out of market
    signal = pd.Series(0, index=prices.index, dtype=float)

    if strategy.indicator == 'SMA_CROSSOVER':
        short_ma = prices.rolling(window=int(p1)).mean()
        long_ma = prices.rolling(window=int(p2)).mean()
        signal = (short_ma > long_ma).astype(float)

    elif strategy.indicator == 'RSI':
        delta = prices.diff()
        gain = delta.clip(lower=0).rolling(window=int(p1)).mean()
        loss = (-delta.clip(upper=0)).rolling(window=int(p1)).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        # Stateful: enter when oversold (<30), exit when overbought (>70)
        position = 0
        for i in range(len(rsi)):
            if pd.isna(rsi.iloc[i]):
                continue
            if position == 0 and rsi.iloc[i] < 30:
                position = 1
            elif position == 1 and rsi.iloc[i] > 70:
                position = 0
            signal.iloc[i] = position

    elif strategy.indicator == 'MOMENTUM':
        # Buy when price is above price N days ago
        signal = (prices > prices.shift(int(p1))).astype(float)

    # Calculate daily strategy returns (signal is shifted by 1 to avoid lookahead)
    daily_returns = prices.pct_change().fillna(0)
    strategy_returns = signal.shift(1).fillna(0) * daily_returns
    cumulative = (1 + strategy_returns).cumprod()

    # Total return %
    total_return = (float(cumulative.iloc[-1]) - 1) * 100 if len(cumulative) > 0 else 0.0

    # Max drawdown %
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = float(drawdown.min()) * 100 if len(drawdown) > 0 else 0.0

    # Count round-trip trades and compute win rate
    trades = []
    in_trade = False
    entry_price = 0.0
    for i in range(len(signal)):
        if signal.iloc[i] == 1 and not in_trade:
            in_trade = True
            entry_price = float(prices.iloc[i])
        elif signal.iloc[i] == 0 and in_trade:
            in_trade = False
            trades.append(float(prices.iloc[i]) - entry_price)

    num_trades = len(trades)
    win_rate = (sum(1 for t in trades if t > 0) / num_trades * 100) if num_trades > 0 else 0.0

    return {
        'total_return': round(total_return, 2),
        'max_drawdown': round(max_drawdown, 2),
        'win_rate': round(win_rate, 2),
        'num_trades': num_trades,
    }


class StockListView(ListView):
    '''Display all stocks in the universe.'''

    model = Stock
    template_name = 'project/stock_list.html'
    context_object_name = 'stocks'


class StockDetailView(DetailView):
    '''Display details for a single stock identified by its ticker.'''

    model = Stock
    template_name = 'project/stock_detail.html'
    context_object_name = 'stock'

    def get_object(self):
        '''Return the Stock with the ticker from the URL.'''
        return get_object_or_404(Stock, ticker=self.kwargs['ticker'])


class InvestorDetailView(DetailView):
    '''Display the investor dashboard showing strategies and screens.'''

    model = Investor
    template_name = 'project/investor_dashboard.html'
    context_object_name = 'investor'

    def get_context_data(self, **kwargs):
        '''Add strategies and screens to context.'''
        context = super().get_context_data(**kwargs)
        context['strategies'] = self.object.get_strategies()
        context['screens'] = self.object.get_screens()
        return context


class StrategyListView(ListView):
    '''Display all strategies for a given investor.'''

    model = Strategy
    template_name = 'project/strategy_list.html'
    context_object_name = 'strategies'

    def get_queryset(self):
        '''Return strategies belonging to the investor in the URL.'''
        return Strategy.objects.filter(investor__pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        '''Add the investor to context.'''
        context = super().get_context_data(**kwargs)
        context['investor'] = get_object_or_404(Investor, pk=self.kwargs['pk'])
        return context


class StrategyDetailView(DetailView):
    '''Display a single strategy and its past backtest results.'''

    model = Strategy
    template_name = 'project/strategy_detail.html'
    context_object_name = 'strategy'

    def get_context_data(self, **kwargs):
        '''Add past backtest results to context.'''
        context = super().get_context_data(**kwargs)
        context['backtests'] = self.object.get_backtests()
        return context


class CreateStrategyView(CreateView):
    '''A view to handle creation of a new Strategy.
    (1) Display the HTML form to the user (GET)
    (2) Process form submission and store the new strategy (POST)
    '''

    form_class = CreateStrategyForm
    template_name = 'project/strategy_form.html'

    def get_context_data(self, **kwargs):
        '''Add investor to context so the template can show ownership.'''
        context = super().get_context_data(**kwargs)
        context['investor'] = get_object_or_404(Investor, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        '''Attach the investor from the URL before saving.'''
        form.instance.investor = get_object_or_404(Investor, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect to the newly created strategy's detail page.'''
        return reverse('strategy_detail', kwargs={'pk': self.object.pk})


class UpdateStrategyView(UpdateView):
    '''A view to handle updating an existing Strategy.'''

    model = Strategy
    form_class = UpdateStrategyForm
    template_name = 'project/strategy_form.html'

    def get_context_data(self, **kwargs):
        '''Add investor to context.'''
        context = super().get_context_data(**kwargs)
        context['investor'] = self.object.investor
        return context

    def get_success_url(self):
        '''Redirect to the updated strategy's detail page.'''
        return reverse('strategy_detail', kwargs={'pk': self.object.pk})


class DeleteStrategyView(DeleteView):
    '''A view to handle deleting a Strategy.'''

    model = Strategy
    template_name = 'project/confirm_delete.html'

    def get_context_data(self, **kwargs):
        '''Add object name and cancel URL to context.'''
        context = super().get_context_data(**kwargs)
        context['object_name'] = str(self.object)
        context['cancel_url'] = reverse('strategy_detail', kwargs={'pk': self.object.pk})
        return context

    def get_success_url(self):
        '''Redirect to the investor's strategy list after deletion.'''
        return reverse('strategy_list', kwargs={'pk': self.object.investor.pk})


class ScreenListView(ListView):
    '''Display all screens for a given investor.'''

    model = Screen
    template_name = 'project/screen_list.html'
    context_object_name = 'screens'

    def get_queryset(self):
        '''Return screens belonging to the investor in the URL.'''
        return Screen.objects.filter(investor__pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        '''Add the investor to context.'''
        context = super().get_context_data(**kwargs)
        context['investor'] = get_object_or_404(Investor, pk=self.kwargs['pk'])
        return context


class CreateScreenView(CreateView):
    '''A view to handle creation of a new Screen.
    (1) Display the HTML form to the user (GET)
    (2) Process form submission and store the new screen (POST)
    '''

    form_class = CreateScreenForm
    template_name = 'project/screen_form.html'

    def get_context_data(self, **kwargs):
        '''Add investor to context.'''
        context = super().get_context_data(**kwargs)
        context['investor'] = get_object_or_404(Investor, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        '''Attach the investor from the URL before saving.'''
        form.instance.investor = get_object_or_404(Investor, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect to run the new screen immediately.'''
        return reverse('run_screener', kwargs={'pk': self.object.pk})


class UpdateScreenView(UpdateView):
    '''A view to handle updating an existing Screen.'''

    model = Screen
    form_class = UpdateScreenForm
    template_name = 'project/screen_form.html'

    def get_context_data(self, **kwargs):
        '''Add investor to context.'''
        context = super().get_context_data(**kwargs)
        context['investor'] = self.object.investor
        return context

    def get_success_url(self):
        '''Redirect to run the updated screen.'''
        return reverse('run_screener', kwargs={'pk': self.object.pk})


class DeleteScreenView(DeleteView):
    '''A view to handle deleting a Screen.'''

    model = Screen
    template_name = 'project/confirm_delete.html'

    def get_context_data(self, **kwargs):
        '''Add object name and cancel URL to context.'''
        context = super().get_context_data(**kwargs)
        context['object_name'] = str(self.object)
        context['cancel_url'] = reverse('run_screener', kwargs={'pk': self.object.pk})
        return context

    def get_success_url(self):
        '''Redirect to the investor's screen list after deletion.'''
        return reverse('screen_list', kwargs={'pk': self.object.investor.pk})


class BacktestResultDetailView(DetailView):
    '''Display the full results of a single backtest run.'''

    model = BacktestResult
    template_name = 'project/backtest_result.html'
    context_object_name = 'result'


def run_screener(request, pk):
    '''Apply a Screen's filters against the Stock universe and display matching results.'''
    screen = get_object_or_404(Screen, pk=pk)
    results = screen.run()
    context = {
        'screen': screen,
        'investor': screen.investor,
        'results': results,
        'result_count': results.count(),
    }
    return render(request, 'project/screen_results.html', context)


def run_backtest(request, pk):
    '''Run a backtest for a given strategy against a user-selected stock and date range.
    (1) Display form to choose stock and date range (GET)
    (2) Fetch Yahoo Finance data, compute metrics, save BacktestResult (POST)
    '''
    strategy = get_object_or_404(Strategy, pk=pk)

    if request.method == 'POST':
        ticker = request.POST.get('ticker')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        stock = get_object_or_404(Stock, ticker=ticker)

        try:
            metrics = _run_backtest_engine(strategy, stock, start_date, end_date)
        except Exception:
            metrics = None

        if metrics:
            result = BacktestResult.objects.create(
                strategy=strategy,
                stock=stock,
                start_date=start_date,
                end_date=end_date,
                total_return=metrics['total_return'],
                max_drawdown=metrics['max_drawdown'],
                win_rate=metrics['win_rate'],
                num_trades=metrics['num_trades'],
            )
            return redirect('backtest_result', pk=result.pk)

        # Engine returned None — bad ticker or no data for that date range
        context = {
            'strategy': strategy,
            'stocks': Stock.objects.all(),
            'error': 'Could not fetch price data. Check the ticker and date range.',
        }
        return render(request, 'project/backtest_form.html', context)

    # GET — display the backtest setup form
    context = {
        'strategy': strategy,
        'stocks': Stock.objects.all(),
    }
    return render(request, 'project/backtest_form.html', context)
