# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencelisting',
            name='earliestPriorityFilingDate',
            field=models.DateField(verbose_name=b'Earliest priority filing date'),
        ),
        migrations.AlterField(
            model_name='sequencelisting',
            name='filingDate',
            field=models.DateField(verbose_name=b'Filing date'),
        ),
        migrations.AlterField(
            model_name='sequencelisting',
            name='productionDate',
            field=models.DateField(verbose_name=b'Production date'),
        ),
    ]
