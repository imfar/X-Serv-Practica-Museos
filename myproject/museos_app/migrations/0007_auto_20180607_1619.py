# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos_app', '0006_auto_20180530_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='museo',
            name='identidad',
        ),
        migrations.AlterField(
            model_name='museo',
            name='descrip',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='museo',
            name='telefono',
            field=models.CharField(max_length=128),
        ),
    ]
