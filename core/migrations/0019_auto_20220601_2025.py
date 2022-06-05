# Generated by Django 2.2.14 on 2022-06-01 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20220601_2005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payment',
            new_name='order',
        ),
        migrations.RemoveField(
            model_name='address',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Order'),
        ),
    ]