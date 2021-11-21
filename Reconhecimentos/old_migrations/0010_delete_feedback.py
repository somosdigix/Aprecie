# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0009_feedback'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Feedback',
        ),
    ]
