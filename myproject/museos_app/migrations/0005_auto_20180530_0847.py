# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('museos_app', '0004_comentario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seleccion',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=128)),
                ('size', models.CharField(max_length=64)),
                ('color', models.CharField(max_length=64)),
                ('name', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='museo',
            name='selecciones',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='seleccion',
            name='museo',
            field=models.ForeignKey(to='museos_app.Museo'),
        ),
        migrations.AddField(
            model_name='seleccion',
            name='user',
            field=models.ForeignKey(to='museos_app.Usuario'),
        ),
    ]
