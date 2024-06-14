from django.urls import path
from .views import *

urlpatterns = [
    path('conversions/', conversions, name='conversions'),
    path('rates/', rates, name='rates'),
    path('exchange_rate/', exchange_rate, name='exchange_rate'),
    path('history/', historical_currency, name='historical_currency'),
    path('available_currencies/', available_currencies, name='available_currencies'),
    path('daily_summary/', daily_summary, name='daily_summary'),
    path('world_population/', world_population, name='world_population'),
]
