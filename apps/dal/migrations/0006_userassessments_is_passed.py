# Generated by Django 5.1.4 on 2025-01-28 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dal', '0005_userassessments_score_percentage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userassessments',
            name='is_passed',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
