# Generated by Django 4.1.2 on 2022-10-26 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clubs", "0007_club_close_time_club_open_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="club",
            name="close_time",
            field=models.PositiveIntegerField(default="", null=True),
        ),
        migrations.AlterField(
            model_name="club",
            name="open_time",
            field=models.PositiveIntegerField(default="", null=True),
        ),
    ]