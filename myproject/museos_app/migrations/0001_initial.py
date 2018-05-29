# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Museos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('id_entidad', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=128)),
                ('descrip', models.TextField()),
            ],
        ),
    ]
