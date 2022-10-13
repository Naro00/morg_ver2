# Generated by Django 4.1.2 on 2022-10-05 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clubs", "0002_alter_club_description"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="amenity",
            options={"verbose_name_plural": "Amenities"},
        ),
        migrations.AddField(
            model_name="club",
            name="name",
            field=models.CharField(default="", max_length=180),
        ),
    ]
