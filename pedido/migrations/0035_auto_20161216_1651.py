# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0034_auto_20161210_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancelarpedido',
            name='motivo',
            field=models.ForeignKey(default=1, to='pedido.MotivoCancelacion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cancelarpedidows',
            name='motivo',
            field=models.ForeignKey(default=1, to='pedido.MotivoCancelacion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cancelarpedido',
            name='imagen',
            field=models.ImageField(null=True, upload_to=b'cancelarp/', blank=True),
        ),
        migrations.AlterField(
            model_name='cancelarpedidows',
            name='imagen',
            field=models.ImageField(null=True, upload_to=b'cancelarpw/', blank=True),
        ),
    ]
