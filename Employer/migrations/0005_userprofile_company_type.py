# Generated by Django 3.2.13 on 2023-07-13 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employer', '0004_auto_20230713_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='company_type',
            field=models.CharField(blank=True, choices=[('employer_private_sector', 'Private Sector')], max_length=500),
        ),
    ]
