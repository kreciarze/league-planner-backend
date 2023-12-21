from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .factories import MatchFactory, SeasonFactory, TeamFactory

pytestmark = [pytest.mark.django_db]


def test_scoreboard(
    api_client: APIClient,
    season_factory: SeasonFactory,
    team_factory: TeamFactory,
    match_factory: MatchFactory,
) -> None:
    season = season_factory.create()
    url = reverse("seasons-detail", args=[season.pk])
    team1 = team_factory.create(
        name="Polska",
        season=season,
    )
    team2 = team_factory.create(
        name="Argentyna",
        season=season,
    )
    team3 = team_factory.create(
        name="Meksyk",
        season=season,
    )
    match_factory.create(
        season=season,
        host=team1,
        visitor=team2,
        host_score=0,
        visitor_score=2,
        datetime=datetime.now(),
    )
    match_factory.create(
        season=season,
        host=team1,
        visitor=team3,
        host_score=0,
        visitor_score=0,
        datetime=datetime.now(),
    )
    match_factory.create(
        season=season,
        host=team3,
        visitor=team2,
        host_score=0,
        visitor_score=2,
        datetime=datetime.now(),
    )
    match_factory.create(
        season=season,
        host=None,
        visitor=None,
        datetime=datetime.now(),
    )
    response = api_client.get(f"{url}scoreboard/")
    assert response.status_code == status.HTTP_200_OK, response
    assert len(response.data["results"]) == 3
    teams = response.data["results"]
    assert teams[0]["name"] == "Argentyna"
    assert teams[1]["name"] == "Meksyk"
    assert teams[2]["name"] == "Polska"
    assert teams[0]["score"] == 6
    assert teams[1]["score"] == 1
    assert teams[2]["score"] == 1
