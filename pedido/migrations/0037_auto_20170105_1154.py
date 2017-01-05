# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0036_auto_20161222_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracionpedido',
            name='descripciontp1',
            field=models.IntegerField(default=1, verbose_name=b'Motorizados planta', choices=[(1, b'Con Descripcion'), (2, b'Sin Descripcion')]),
        ),
        migrations.AddField(
            model_name='configuracionpedido',
            name='descripciontp2',
            field=models.IntegerField(default=1, verbose_name=b'Motorizados suscripcion', choices=[(1, b'Con Descripcion'), (2, b'Sin Descripcion')]),
        ),
    ]
