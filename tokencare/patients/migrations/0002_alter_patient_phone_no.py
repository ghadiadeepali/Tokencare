# Generated by Django 4.2.23 on 2025-06-28 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='phone_no',
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
    ]
