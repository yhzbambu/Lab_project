from django.contrib import admin

from .models import Video_Tube,Video_Tag,Video_Type

from .models import Video_Tube,Video_Tag,Video_Type,WatchNumber

# Register your models here.
@admin.register(Video_Type)
class VideoTypeAdin(admin.ModelAdmin):
    list_display=('id','type_name')
@admin.register(Video_Tag)
class VideoTagAdmin(admin.ModelAdmin):
    list_display=('id','tag_language','tag_level','tag_is_chinese')
@admin.register(Video_Tube)
class VideoTubeAdmin(admin.ModelAdmin):
    list_display=('id','title','author','video_type','created_time','last_updated_time','get_watch_number','tag','video_id','video_url')

# @admin.register(WatchNumber)
# class WatchNumberAdmin(admin.ModelAdmin):
#     list_display=('watch_number','video')

