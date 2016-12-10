# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0015_tienda_token'),
        ('pedido', '0031_auto_20160722_1729'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionPedido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tirillatp1', models.IntegerField(default=1, verbose_name=b'Motorizados planta', choices=[(1, b'Con total'), (2, b'Sin total')])),
                ('tirillatp2', models.IntegerField(default=1, verbose_name=b'Motorizados suscripcion', choices=[(1, b'Con total'), (2, b'Sin total')])),
                ('cerrartp1', models.IntegerField(default=1, verbose_name=b'Motorizados planta', choices=[(1, b'Con Foto'), (2, b'Con Bot\xc3\xb3n')])),
                ('cerrartp2', models.IntegerField(default=1, verbose_name=b'Motorizados suscripcion', choices=[(1, b'Con Foto'), (2, b'Con Bot\xc3\xb3n')])),
                ('empresa', models.ForeignKey(to='usuario.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='MotivoCancelacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=300)),
                ('descripcion', models.CharField(max_length=800)),
                ('estado', models.BooleanField(default=True)),
                ('configuracion', models.ForeignKey(to='pedido.ConfiguracionPedido')),
            ],
        ),
    ]
