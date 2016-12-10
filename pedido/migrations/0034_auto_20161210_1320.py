# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0033_configuracionpedido_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motivocancelacion',
            name='descripcion',
            field=models.CharField(max_length=800, null=True, blank=True),
        ),
    ]
