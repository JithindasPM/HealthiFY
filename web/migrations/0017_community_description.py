# Generated by Django 5.0.3 on 2025-02-19 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0016_community'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
