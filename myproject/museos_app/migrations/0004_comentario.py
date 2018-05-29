# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos_app', '0003_auto_20180526_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('texto', models.TextField()),
                ('museo', models.ForeignKey(to='museos_app.Museo')),
            ],
        ),
    ]
