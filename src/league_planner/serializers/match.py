from rest_framework import serializers

from league_planner.models.match import Match
from league_planner.models.season import Season
from league_planner.models.team import Team
from league_planner.serializers.season import SeasonSerializer
from league_planner.serializers.team import TeamSerializer
from league_planner.settings import DEFAULT_DATETIME_FORMAT


class MatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  # noqa: A003
    season = serializers.PrimaryKeyRelatedField(queryset=Season.objects.all())
    host = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        required=False,
    )
    visitor = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        required=False,
    )
    host_score = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    visitor_score = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    address = serializers.CharField(
        max_length=50,
        required=False,
    )
    datetime = serializers.DateTimeField(
        required=False,
        format=DEFAULT_DATETIME_FORMAT,
    )

    class Meta:
        model = Match
        fields = (
            "id",
            "season",
            "host",
            "host_score",
            "visitor",
            "visitor_score",
            "address",
            "datetime",
        )


class MatchDetailSerializer(MatchSerializer):
    season = SeasonSerializer(read_only=True)
    host = TeamSerializer(read_only=True)
    visitor = TeamSerializer(read_only=True)
