# Generated by Django 2.1.7 on 2019-07-15 14:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='basic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('sexy', models.CharField(max_length=10)),
                ('birthday', models.CharField(max_length=10)),
                ('constellation', models.CharField(max_length=10)),
                ('blood', models.CharField(max_length=10)),
                ('Email', models.EmailField(max_length=254)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='boss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mom', models.TextField()),
                ('bobo', models.TextField()),
                ('money', models.TextField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='school',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Kindergarten', models.CharField(max_length=20)),
                ('Elementary', models.CharField(max_length=20)),
                ('junior', models.CharField(max_length=20)),
                ('senior', models.CharField(max_length=20)),
                ('university', models.CharField(max_length=20)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work1', models.CharField(max_length=20)),
                ('work2', models.CharField(max_length=20)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]