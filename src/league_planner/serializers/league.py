from django.contrib.auth.models import User
from rest_framework import serializers

from league_planner.models.league import League


class LeagueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  # noqa: A003
    name = serializers.CharField()
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    owner_login = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = League
        fields = ("id", "name", "owner", "owner_login")
