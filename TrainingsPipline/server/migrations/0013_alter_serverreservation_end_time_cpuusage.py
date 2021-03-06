# Generated by Django 4.0 on 2021-12-14 07:36

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0012_remove_servermanagement_server name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverreservation',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 14, 9, 36, 1, 247709, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='CpuUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu', models.FloatField(default=0)),
                ('ram', models.FloatField(default=0)),
                ('server_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.servermanagement')),
            ],
        ),
    ]
