# Generated by Django 4.2.6 on 2023-12-12 19:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("league_planner", "0010_team_number"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="team",
            options={"ordering": ["number"]},
        ),
        migrations.AddField(
            model_name="team",
            name="image",
            field=models.ImageField(null=True, upload_to="images/teams/"),
        ),
    ]
