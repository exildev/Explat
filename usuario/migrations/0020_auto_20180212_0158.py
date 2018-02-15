# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0019_accesoplataforma_emp'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesoplataforma',
            name='tienda',
            field=models.ForeignKey(blank=True, to='usuario.Tienda', null=True),
        ),
        migrations.AlterField(
            model_name='accesoplataforma',
            name='emp',
            field=models.ForeignKey(verbose_name=b'Empresa', to='usuario.Empresa'),
        ),
    ]
