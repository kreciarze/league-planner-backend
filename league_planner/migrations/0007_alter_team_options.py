# Generated by Django 4.1.3 on 2022-11-15 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league_planner', '0006_alter_team_city'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['id']},
        ),
    ]
