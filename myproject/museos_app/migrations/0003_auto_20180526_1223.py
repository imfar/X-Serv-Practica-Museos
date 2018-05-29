# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos_app', '0002_museos_disp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('identidad', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=128)),
                ('descrip', models.TextField()),
                ('access', models.CharField(max_length=1)),
                ('link', models.CharField(max_length=512)),
                ('direccion', models.TextField()),
                ('barrio', models.CharField(max_length=128)),
                ('distrito', models.CharField(max_length=128)),
                ('telefono', models.CharField(max_length=9)),
                ('email', models.CharField(max_length=128)),
            ],
        ),
        migrations.DeleteModel(
            name='Museos',
        ),
    ]
