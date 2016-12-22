# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0016_auto_20161210_1259'),
        ('motorizado', '0003_motorizado_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('soat', models.IntegerField()),
                ('empresa', models.ForeignKey(to='usuario.Empresa')),
            ],
        ),
    ]
