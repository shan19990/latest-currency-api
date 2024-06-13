
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('getapitoken/<str:email>/', CreateNewTokenView.as_view(), name='create_email_token'),
]
