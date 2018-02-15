# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0020_auto_20180212_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesoplataforma',
            name='emp',
            field=models.ForeignKey(verbose_name=b'Empresa', blank=True, to='usuario.Empresa', null=True),
        ),
    ]
