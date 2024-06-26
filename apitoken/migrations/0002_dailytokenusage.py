# Generated by Django 5.0.6 on 2024-06-16 15:28

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitoken', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyTokenUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('usage_count', models.IntegerField(default=0)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apitoken.apitoken')),
            ],
            options={
                'unique_together': {('token', 'date')},
            },
        ),
    ]
