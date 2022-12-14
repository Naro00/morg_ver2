# Generated by Django 4.1.2 on 2022-10-25 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="email_secret",
            field=models.CharField(blank=True, default="", max_length=20),
        ),
        migrations.AddField(
            model_name="user",
            name="email_verified",
            field=models.BooleanField(default=False),
        ),
    ]
