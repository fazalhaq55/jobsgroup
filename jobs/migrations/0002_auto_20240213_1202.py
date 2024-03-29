# Generated by Django 3.2.13 on 2024-02-13 07:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info',
            name='activation_date',
        ),
        migrations.RemoveField(
            model_name='info',
            name='org_photo',
        ),
        migrations.RemoveField(
            model_name='info',
            name='posted_by',
        ),
        migrations.RemoveField(
            model_name='info',
            name='status',
        ),
        migrations.AddField(
            model_name='info',
            name='company_industry',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='company_type',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='grade',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='posted_date',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='About_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='job_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 2, 13, 7, 32, 24, 696885, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='info',
            name='job_descriptions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='job_requirements',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='submission_guidelines',
            field=models.TextField(blank=True, null=True),
        ),
    ]
