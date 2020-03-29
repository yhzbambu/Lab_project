from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Video_Type(models.Model):
    type_name=models.CharField(max_length=15)
    def __str__(self):
        return self.type_name
class Video_Tag(models.Model):
    tag_language=models.CharField(max_length=10)
    tag_level=models.CharField(max_length=10)
    tag_is_chinese=models.CharField(max_length=5)
    def __str__(self):
        return "%s %s %s" %(self.tag_language,self.tag_level,self.tag_is_chinese)

class Video_Tube(models.Model):
    title=models.CharField(max_length=50)
    
    # content=models.TextField(default=50)
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    created_time=models.DateTimeField(auto_now_add=True)
    last_updated_time=models.DateTimeField(auto_now_add=True)
    # is_deleted=models.BooleanField(default=False)
    # watch_number=models.IntegerField(default=0)
    video_type=models.ForeignKey(Video_Type,on_delete=models.DO_NOTHING,null=True)
    tag=models.ForeignKey(Video_Tag,on_delete=models.DO_NOTHING,null=True)
    video_id=models.CharField(max_length=50, null=True)
    video_url=models.CharField(max_length=200,null=True)
    def __str__(self):
        return "<Video_Tube:%s>" % self.title
    video_type=models.ForeignKey(Video_Type,on_delete=models.DO_NOTHING,null=True)
    tag=models.ForeignKey(Video_Tag,on_delete=models.DO_NOTHING,null=True)
    # 下面外建模型以小寫表示
            # video=video.objects.all()[2]
        # video.watchnumber 
        # 會報錯
    def get_watch_number(self):

        # return self.watchnumber.watch_number
        try:
            return self.watchnumber.watch_number
        except Exception as e:
            return 0
    def __str__(self):
        return "<Video_Tube:%s>" % self.title

    class Meta:
        ordering=['-created_time']
# 為了防止在後台改數據時候 影響到前台在計數
class WatchNumber(models.Model):
    watch_number= models.IntegerField(default=0)
    video =models.OneToOneField(Video_Tube,on_delete=models.DO_NOTHING,null=True)
