from django.db import models
from rest_framework.authtoken.admin import User

from league_planner.models.league import League


class Season(models.Model):
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        verbose_name="Season belong to that League",
    )
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    start_date = models.DateField(
        verbose_name="Start date of season",
        null=True,
    )
    end_date = models.DateField(
        verbose_name="End date of season",
        null=True,
    )
    points_per_win = models.PositiveSmallIntegerField(
        verbose_name="Points per win",
        default=3,
    )
    points_per_draw = models.PositiveSmallIntegerField(
        verbose_name="Points per draw",
        default=1,
    )
    points_per_lose = models.PositiveSmallIntegerField(
        verbose_name="Points per lose",
        default=0,
    )

    class Meta:
        ordering = ["start_date"]

    def is_owner(self, user: User) -> bool:
        return self.league.is_owner(user)
