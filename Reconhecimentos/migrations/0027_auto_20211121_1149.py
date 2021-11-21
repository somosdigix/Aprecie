# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0026_auto_20211121_1149'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FeedbackSimplificado',
            new_name='Feedback',
        ),
    ]
