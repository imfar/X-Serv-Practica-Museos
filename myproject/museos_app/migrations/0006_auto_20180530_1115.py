# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos_app', '0005_auto_20180530_0847'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seleccion',
            old_name='user',
            new_name='usuario',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='name',
        ),
        migrations.AddField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='color',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='size',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='titulo',
            field=models.CharField(default='', max_length=128),
        ),
    ]
