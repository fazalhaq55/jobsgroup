# Generated by Django 3.2.13 on 2024-02-13 08:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0004_alter_detail_scho_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='scho_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 2, 13, 8, 14, 39, 678463, tzinfo=utc)),
        ),
    ]