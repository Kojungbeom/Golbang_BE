# Generated by Django 4.2.14 on 2024-08-28 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("participants", "0010_remove_participant_points"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="points",
            field=models.IntegerField(default=0, verbose_name="포인트"),
        ),
    ]
