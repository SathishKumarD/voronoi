# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 01:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0007_auto_20161206_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='baths',
            field=models.FloatField(choices=[(1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (2.5, 2.5), (3.0, 3.0), (3.5, 3.5)], default=1, null=True, verbose_name='Baths'),
        ),
    ]
