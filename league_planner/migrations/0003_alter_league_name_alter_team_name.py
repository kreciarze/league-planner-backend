# Generated by Django 4.1.3 on 2022-11-15 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_planner', '0002_alter_league_owner_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
