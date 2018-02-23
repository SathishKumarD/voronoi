from django.contrib import admin

# Register your models here.

from .models import House
from .models import BusStop
from .models import UserProfile

admin.site.register(House)
admin.site.register(BusStop)
admin.site.register(UserProfile)