from django.db import models
from rest_framework.authtoken.admin import User

from league_planner.models.season import Season


class Match(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        verbose_name="Match belong to that Season",
    )
    host = models.ForeignKey(
        "league_planner.Team",
        on_delete=models.SET_NULL,
        verbose_name="Host Team",
        related_name="host",
        null=True,
    )
    visitor = models.ForeignKey(
        "league_planner.Team",
        on_delete=models.SET_NULL,
        verbose_name="Visitor Team",
        related_name="visitor",
        null=True,
    )
    host_score = models.IntegerField(
        verbose_name="Score of host Team",
        null=True,
    )
    visitor_score = models.IntegerField(
        verbose_name="Score of visitor Team",
        null=True,
    )
    address = models.CharField(
        max_length=100,
        verbose_name="Place where match is played",
        null=True,
    )
    datetime = models.DateTimeField(
        verbose_name="Time when match is played",
        null=True,
    )

    class Meta:
        ordering = ["datetime"]
        verbose_name_plural = "matches"

    def is_owner(self, user: User) -> bool:
        return self.season.is_owner(user)
