# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0032_configuracionpedido_motivocancelacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracionpedido',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
