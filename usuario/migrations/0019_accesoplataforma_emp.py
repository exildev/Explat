# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0018_remove_accesoplataforma_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesoplataforma',
            name='emp',
            field=models.ForeignKey(default=1, to='usuario.Empresa'),
            preserve_default=False,
        ),
    ]
