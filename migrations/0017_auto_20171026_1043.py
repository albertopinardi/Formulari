# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-26 08:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulari', '0016_auto_20171002_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anagrafica',
            name='mail',
            field=models.EmailField(max_length=200),
        ),
    ]
