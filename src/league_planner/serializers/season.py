from rest_framework import serializers

from league_planner.models.league import League
from league_planner.models.season import Season
from league_planner.settings import DEFAULT_DATETIME_FORMAT


class SeasonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  # noqa: A003
    league = serializers.PrimaryKeyRelatedField(queryset=League.objects.all())
    name = serializers.CharField()
    start_date = serializers.DateTimeField(
        required=False,
        format=DEFAULT_DATETIME_FORMAT,
    )
    end_date = serializers.DateTimeField(
        required=False,
        format=DEFAULT_DATETIME_FORMAT,
    )
    points_per_win = serializers.IntegerField(
        required=False,
    )
    points_per_draw = serializers.IntegerField(
        required=False,
    )
    points_per_lose = serializers.IntegerField(
        required=False,
    )

    class Meta:
        model = Season
        fields = (
            "id",
            "name",
            "start_date",
            "end_date",
            "league",
            "points_per_win",
            "points_per_draw",
            "points_per_lose",
        )
