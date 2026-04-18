# File: project/urls.py
# Author: Yash Kedia (yashkedi@bu.edu), 4/18/26
# Description: URL patterns for the Stock Screener and Backtesting Platform

from django.urls import path
from .views import *

urlpatterns = [
    # Stock URLs
    path('stocks/', StockListView.as_view(), name='stock_list'),
    path('stocks/<str:ticker>/', StockDetailView.as_view(), name='stock_detail'),

    # Investor dashboard
    path('investor/<int:pk>/', InvestorDetailView.as_view(), name='investor_dashboard'),

    # Strategy URLs
    path('investor/<int:pk>/strategies/', StrategyListView.as_view(), name='strategy_list'),
    path('investor/<int:pk>/strategies/create/', CreateStrategyView.as_view(), name='create_strategy'),
    path('strategies/<int:pk>/', StrategyDetailView.as_view(), name='strategy_detail'),
    path('strategies/<int:pk>/update/', UpdateStrategyView.as_view(), name='update_strategy'),
    path('strategies/<int:pk>/delete/', DeleteStrategyView.as_view(), name='delete_strategy'),
    path('strategies/<int:pk>/backtest/', run_backtest, name='run_backtest'),

    # Screen URLs
    path('investor/<int:pk>/screens/', ScreenListView.as_view(), name='screen_list'),
    path('investor/<int:pk>/screens/create/', CreateScreenView.as_view(), name='create_screen'),
    path('screens/<int:pk>/update/', UpdateScreenView.as_view(), name='update_screen'),
    path('screens/<int:pk>/delete/', DeleteScreenView.as_view(), name='delete_screen'),
    path('screens/<int:pk>/run/', run_screener, name='run_screener'),

    # Backtest result
    path('backtests/<int:pk>/', BacktestResultDetailView.as_view(), name='backtest_result'),
]
