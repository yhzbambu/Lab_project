from django.db import models


# Create your models here.

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class WatchNumber(models.Model):
    watch_number= models.IntegerField(default=0)
    content_type=models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
    

