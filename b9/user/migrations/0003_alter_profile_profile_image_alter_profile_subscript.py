# Generated by Django 4.2 on 2023-04-11 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_follow_profile_follows"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_image",
            field=models.ImageField(null=True, upload_to="", verbose_name="유저이미지"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="subscript",
            field=models.CharField(
                blank=True, max_length=200, verbose_name="유저소개문(짧게)"
            ),
        ),
    ]