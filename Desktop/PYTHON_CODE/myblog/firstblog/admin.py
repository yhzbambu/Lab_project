from django.contrib import admin
from .models import basic,school,work,boss,home,Mood,post
# Register your models here.

admin.site.register(basic)
admin.site.register(school)
admin.site.register(work)
admin.site.register(boss)
admin.site.register(home)
class PostAdmin(admin.ModelAdmin):
    list_display=('nickname', 'message', 'enable', 'pub_time')
    ordering=('-pub_time',)
admin.site.register(Mood)
admin.site.register(post, PostAdmin)