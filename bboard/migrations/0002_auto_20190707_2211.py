# Generated by Django 2.2.3 on 2019-07-07 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='slug',
            field=models.SlugField(default='', max_length=150, unique=True, verbose_name='Slug'),
        ),
    ]
