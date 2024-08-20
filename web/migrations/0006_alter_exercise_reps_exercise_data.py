# Generated by Django 5.0.3 on 2024-08-20 09:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_exercise'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='reps',
            field=models.PositiveIntegerField(blank=True, default=25, null=True),
        ),
        migrations.CreateModel(
            name='Exercise_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
