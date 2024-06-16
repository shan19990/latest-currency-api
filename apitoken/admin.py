from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(EmailModel)
admin.site.register(APIToken)
admin.site.register(DailyTokenUsage)