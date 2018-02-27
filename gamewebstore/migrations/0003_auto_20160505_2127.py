# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamewebstore', '0002_userdata_usergameownership'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onlinegame',
            name='categories',
        ),
        migrations.AddField(
            model_name='onlinegame',
            name='categories',
            field=models.ManyToManyField(related_name='games', to='gamewebstore.Category'),
        ),
    ]
