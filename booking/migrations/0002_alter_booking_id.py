# Generated by Django 5.0.3 on 2024-03-26 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='id',
            field=models.BigIntegerField(editable=False, primary_key=True, serialize=False),
        ),
    ]
