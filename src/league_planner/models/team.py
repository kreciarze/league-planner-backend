from django.db import models


class Team(models.Model):
    league = models.ForeignKey(
        "league_planner.League",
        on_delete=models.CASCADE,
        verbose_name="Team belong to that League",
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
