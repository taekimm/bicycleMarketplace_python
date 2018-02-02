from django.contrib import admin

from .models import User, Bike, BotD
# Register your models here.

admin.site.register(User)
admin.site.register(Bike)
admin.site.register(BotD)
