# Generated by Django 3.0.4 on 2020-03-19 00:35

import budget.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='start_date',
            field=models.DateField(blank=True, default=budget.models.this_year, null=True),
        ),
    ]
