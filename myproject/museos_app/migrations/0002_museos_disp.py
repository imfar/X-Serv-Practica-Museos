# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='museos',
            name='disp',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
