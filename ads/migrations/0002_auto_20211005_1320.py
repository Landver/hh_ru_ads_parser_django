# Generated by Django 3.1.6 on 2021-10-05 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ad',
            options={'get_latest_by': 'created_date'},
        ),
    ]