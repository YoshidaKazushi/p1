# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-19 22:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20160919_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='upload_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date uploaded'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='picture',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app1.PictureTag'),
        ),
    ]