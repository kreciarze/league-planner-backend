from rest_framework import serializers

from league_planner.models.season import Season
from league_planner.models.team import Team


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  # noqa: A003
    season = serializers.PrimaryKeyRelatedField(queryset=Season.objects.all())
    name = serializers.CharField()
    city = serializers.CharField(required=False)
    number = serializers.IntegerField(required=False)

    class Meta:
        model = Team
        fields = ("id", "season", "name", "city", "number")


class TeamImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

    class Meta:
        model = Team
        fields = ("image",)

    def update(self, instance: Team, validated_data: dict) -> Team:
        instance.image = validated_data.get("image", instance.image)
        instance.image.name = f"team_{instance.id}.png"
        instance.save()
        return instance


class ScoreboardSerializer(TeamSerializer):
    score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = ("id", "season", "name", "city", "number", "score")
