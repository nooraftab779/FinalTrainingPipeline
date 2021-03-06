# Generated by Django 4.0 on 2021-12-09 09:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_servermanagement_occupied_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='serverreservation',
            old_name='server',
            new_name='server_id',
        ),
        migrations.RenameField(
            model_name='serverreservation',
            old_name='user_name',
            new_name='user_id',
        ),
        migrations.RemoveField(
            model_name='servermanagement',
            name='occupied_time',
        ),
        migrations.AddField(
            model_name='servermanagement',
            name='enable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='serverreservation',
            name='end_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='serverreservation',
            name='reservation_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 9, 9, 40, 27, 413789, tzinfo=utc)),
        ),
    ]
