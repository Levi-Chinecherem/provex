# Generated by Django 5.0.1 on 2024-01-21 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_funds'),
    ]

    operations = [
        migrations.AddField(
            model_name='funds',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
