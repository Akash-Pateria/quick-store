# Generated by Django 2.2.11 on 2020-03-30 16:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20200329_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='filetuple',
            name='heartbeatCount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
