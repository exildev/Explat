# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0017_accesoplataforma'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accesoplataforma',
            name='empresa',
        ),
    ]
