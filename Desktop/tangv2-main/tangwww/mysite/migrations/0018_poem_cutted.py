# Generated by Django 3.0.1 on 2020-12-26 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0017_auto_20201224_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='poem',
            name='cutted',
            field=models.TextField(blank=True),
        ),
    ]