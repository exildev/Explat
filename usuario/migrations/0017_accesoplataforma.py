# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0016_auto_20161210_1259'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccesoPlataforma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idenficacion', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=20)),
                ('identificador', models.CharField(max_length=30)),
                ('status', models.BooleanField(default=True)),
                ('autorizado', models.BooleanField(default=False)),
                ('empresa', models.ForeignKey(to='usuario.Empresa')),
            ],
            options={
                'verbose_name': 'Solicitud de acceso',
                'verbose_name_plural': 'Solicitudes de accesos',
            },
        ),
    ]
