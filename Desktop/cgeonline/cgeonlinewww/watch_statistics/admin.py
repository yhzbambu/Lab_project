from django.contrib import admin


# Register your models here.

from .models import WatchNumber
# Register your models here.

@admin.register(WatchNumber)
class WatchNumberAdmin(admin.ModelAdmin):
    list_display=('watch_number','content_object')

