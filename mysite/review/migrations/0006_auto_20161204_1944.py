# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-04 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0005_auto_20161204_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(max_length=1024, verbose_name='Review the house'),
        ),
    ]