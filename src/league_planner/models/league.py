from django.contrib.auth.models import User
from django.db import models


class League(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Owner of League",
        related_name="owners",
    )

    class Meta:
        ordering = ["id"]

    def is_owner(self, user: User) -> bool:
        return user == self.owner
