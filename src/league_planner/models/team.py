from django.db import models
from rest_framework.authtoken.admin import User

from league_planner.models.season import Season


class Team(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        verbose_name="Team belong to that Season",
    )
    name = models.CharField(
        max_length=50,
        default=None,
        unique=True,
    )
    city = models.CharField(
        max_length=50,
        default="Not Set",
    )
    number = models.IntegerField(
        null=True,
    )
    image = models.ImageField(
        upload_to="images/teams/",
        null=True,
    )

    class Meta:
        ordering = ["number"]

    def is_owner(self, user: User) -> bool:
        return self.season.is_owner(user)
