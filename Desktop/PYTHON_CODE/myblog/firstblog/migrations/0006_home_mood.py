# Generated by Django 2.1.7 on 2019-07-25 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstblog', '0005_mood_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='mood',
            field=models.CharField(default='幹', max_length=10),
        ),
    ]
