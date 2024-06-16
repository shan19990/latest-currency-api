from django.urls import path
from .views import *

urlpatterns = [
    path('conversions/', conversions, name='conversions'),
    path('rates/', rates, name='rates'),
    path('exchange_rate/', exchange_rate, name='exchange_rate'),
    path('history/', historical_currency, name='historical_currency'),
    path('available_currencies/', available_currencies, name='available_currencies'),
    path('daily_summary/', daily_summary, name='daily_summary'),

    path('world/live/', world_population, name='world_population'),
    path('world/live/top20/', world_top20_population, name='world_top20_population'),
    path('world/historical/', world_historical, name='world_historical'),
    path('world/forecast/', world_forecast, name='world_forecast'),
    path('country/list/', country_links, name='country_links'),
    path('country/live/', country_population, name='country_population'),
    path('country/historical/', country_historical, name='country_historical'),
    path('country/historical/statistic/', country_historican_statistic, name='country_historican_statistic'),
    path('country/forecast/statistic/', country_forecast_statistic, name='country_forecast_statistic'),
    path('country/city/', country_city_population, name='country_city_population'),
    path('country/counts/', country_counts, name='country_counts'),
    path('country/flags/', country_flags, name='country_flags'),

    path('location/', receive_location, name='location'),
    path('location/<str:ip_address>/', ip_geolocation, name='ip_geolocation'),

    path('crpto/live/', crypto_currency, name='crypto_currency'),
]
