# Generated by Django 5.1.4 on 2025-06-24 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dal', '0027_alter_leaderboardentry_total_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaderboardentry',
            name='total_score',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
