# Generated by Django 3.2.5 on 2021-12-14 09:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0012_remove_servermanagement_server name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverreservation',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 14, 11, 36, 1, 160726, tzinfo=utc)),
        ),
    ]
