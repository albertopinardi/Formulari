# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-14 08:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulari', '0018_auto_20171026_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulari',
            name='stato',
            field=models.CharField(choices=[('AP', 'Aperto'), ('RP', 'Riepilogato'), ('CH', 'Chiuso'), ('ER', 'Errore'), ('IA', 'Inattivo'), ('ND', 'No Documenti')], default='AP', max_length=2),
        ),
    ]
