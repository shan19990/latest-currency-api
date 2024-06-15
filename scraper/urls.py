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
    path('country/', country, name='country'),
    path('country_cities/', country_cities, name='country_cities'),
    path('world_cities/', world_cities, name='world_cities'),
    path('country_historic/', country_historic, name='country_historic'),
    path('country_future/', country_future, name='country_future'),
    path('continent/', continent, name='continent'),

    path('location/', receive_location, name='location'),
]
