# Generated by Django 2.2.14 on 2022-06-01 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20220601_2025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
    ]
