# Generated by Django 2.2.5 on 2020-09-12 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_auto_20200912_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poem',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]