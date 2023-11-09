# Generated by Django 3.1.3 on 2021-04-10 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('company', models.CharField(blank=True, max_length=1000, null=True)),
                ('filename', models.FileField(upload_to='')),
            ],
        ),
    ]
