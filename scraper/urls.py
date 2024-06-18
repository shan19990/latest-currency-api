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
    path('world/cities/', world_cities, name='world_cities'),

    path('country/list/', country_links, name='country_links'),
    path('country/live/', country_population, name='country_population'),
    path('country/statistic/', country, name='country'),
    path('country/historical/', country_historical, name='country_historical'),
    path('country/historical/statistic/', country_historican_statistic, name='country_historican_statistic'),
    path('country/forecast/statistic/', country_forecast_statistic, name='country_forecast_statistic'),
    path('country/city/', country_city_population, name='country_city_population'),
    path('country/counts/', country_counts, name='country_counts'),
    path('country/flags/', country_flags, name='country_flags'),

    path('location/', receive_location, name='location'),
    path('location/<str:ip_address>/', ip_geolocation, name='ip_geolocation'),

    path('crypto/live/', crypto_currency, name='crypto_currency'),
    path('crypto/individual/live/', crypto_currency_individual, name='crypto_currency_individual'),

    path('commodities/metals/', commodities_metals, name='commodities_metals'),
    path('commodities/metals/currency/', commodities_metals_currency, name='commodities_metals_currency'),

    path('time/capitals/', time_capitals, name='time_capitals'),
    path('time/popular/', time_popular, name='time_popular'),
    path('time/extended/', time_extended, name='time_extended'),
    path('time/country/', time_country, name='time_country'),
    path('time/country/city/', time_country_city, name='time_country_city'),

    path('weather/capitals/', weather_capitals, name='weather_capitals'),
    path('weather/popular/', weather_popular, name='weather_popular'),
    path('weather/extended/', weather_extended, name='weather_extended'),
    path('weather/country/city/today/', weather_country_city_today, name='weather_country_city_today'),
    path('weather/country/city/forecast/', weather_country_city_forecast, name='weather_country_city_forecast'),

]
