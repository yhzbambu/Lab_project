from django.db import models
from django.utils import timezone
# Create your models here.

class home(models.Model):
    basicinformation = models.CharField(max_length=10)
    schoolinformation = models.CharField(max_length=10)
    workinformation = models.CharField(max_length=10)
    sandybossinformation = models.CharField(max_length=10)
    mood = models.CharField(max_length=10)
    email = models.CharField(max_length=10)
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta0:
        ordering0 = ('-pub_date0',)

class basic(models.Model):
    name = models.CharField(max_length=10)
    sexy = models.CharField(max_length=10)
    birthday = models.CharField(max_length=10)
    constellation = models.CharField(max_length=10)
    blood = models.CharField(max_length=10)
    Email = models.EmailField()
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-pub_date',)

class school(models.Model):
    Kindergarten = models.CharField(max_length=20)
    Elementary = models.CharField(max_length=20)
    junior = models.CharField(max_length=20)
    senior = models.CharField(max_length=20)
    university = models.CharField(max_length=20)
    pub_date1 = models.DateTimeField(default=timezone.now)

    class Meta1:
        ordering1 = ('-pub_date1',)

class work(models.Model):
    work1 = models.CharField(max_length=20)
    work2 = models.CharField(max_length=20)
    pub_date2 = models.DateTimeField(default=timezone.now)

    class Meta2:
        ordering2 = ('-pub_date2',)

class boss(models.Model):
    mom = models.TextField()
    bobo = models.TextField()
    money = models.TextField()
    pub_date3 = models.DateTimeField(default=timezone.now)

    class Meta3:
        ordering3 = ('-pub_date3',)

class Mood(models.Model):
    status = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.status

class post(models.Model):
    mood = models.ForeignKey('Mood', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, default='不願意透漏身分的人')
    message =  models.TextField(null=False)
    del_pass = models.CharField(max_length=10)
    pub_time = models.DateTimeField(auto_now=True)
    enable = models.BooleanField(default=False)

    def __str__(self):
        return self.message