# Generated by Django 4.1.2 on 2022-10-26 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clubs", "0008_alter_club_close_time_alter_club_open_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="club",
            name="close_time",
            field=models.CharField(default="", max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="club",
            name="open_time",
            field=models.CharField(default="", max_length=20, null=True),
        ),
    ]
