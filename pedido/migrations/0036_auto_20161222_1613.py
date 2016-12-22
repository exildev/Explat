# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0035_auto_20161216_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancelarpedido',
            name='observacion',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cancelarpedidows',
            name='observacion',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracionpedido',
            name='cancelartp1',
            field=models.IntegerField(default=1, verbose_name=b'Motorizados planta', choices=[(1, b'Con Foto'), (2, b'Con Bot\xc3\xb3n')]),
        ),
        migrations.AddField(
            model_name='configuracionpedido',
            name='cancelartp2',
            field=models.IntegerField(default=1, verbose_name=b'Motorizados suscripcion', choices=[(1, b'Con Foto'), (2, b'Con Bot\xc3\xb3n')]),
        ),
        migrations.AlterField(
            model_name='confirmarpedido',
            name='imagen',
            field=models.ImageField(null=True, upload_to=b'confirmarpedido/', blank=True),
        ),
    ]
