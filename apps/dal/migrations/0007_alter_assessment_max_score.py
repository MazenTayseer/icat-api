# Generated by Django 5.1.4 on 2025-01-28 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dal', '0006_userassessments_is_passed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='max_score',
            field=models.IntegerField(default=0),
        ),
    ]
