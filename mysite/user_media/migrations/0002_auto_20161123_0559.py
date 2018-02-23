# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 05:59
from __future__ import unicode_literals

from django.db import migrations, models
import user_media.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_media', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermediaimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=user_media.models.get_image_file_path, verbose_name='Image'),
        ),
    ]
