# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-27 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulari', '0007_auto_20170827_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulari',
            name='data',
            field=models.DateField(),
        ),
    ]
