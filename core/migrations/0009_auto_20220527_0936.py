# Generated by Django 2.2.14 on 2022-05-27 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20220527_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('N', 'non'), ('D', 'danger')], max_length=1),
        ),
    ]
