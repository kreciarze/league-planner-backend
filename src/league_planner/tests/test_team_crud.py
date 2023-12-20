from typing import TYPE_CHECKING

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from league_planner.models.team import Team

from .factories import LeagueFactory, MatchFactory, TeamFactory

if TYPE_CHECKING:
    from django.contrib.auth.models import User

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def create_team_data() -> dict:
    return {"name": "RKS Chuwdu", "city": "Kurwix"}


def test_teams_list(api_client: "APIClient", league_factory: "LeagueFactory", team_factory: "TeamFactory") -> None:
    url = reverse("teams-list")
    league = league_factory.create()
    for i in range(10):
        team_factory.create(
            name=f"team{i}",
            league=league,
        )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["count"] == 10


def test_teams_filtering(api_client: "APIClient", league_factory: "LeagueFactory", team_factory: "TeamFactory") -> None:
    url = reverse("teams-list")
    league1 = league_factory.create(name="NBA")
    league2 = league_factory.create(name="WNBA")
    for i in range(5):
        team_factory.create(
            name=f"NBA team{i}",
            league=league1,
        )
    for i in range(5):
        team_factory.create(
            name=f"WNBA team{i}",
            league=league2,
        )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["count"] == 10
    response = api_client.get(f"{url}?league={league1.pk}")
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["count"] == 5
    assert response.data["results"][0]["league"] == league1.pk
    assert response.data["results"][0]["name"] is not None
    assert response.data["results"][0]["city"] is not None
    assert response.data["results"][0]["number"] is None
    assert "image" not in response.data["results"][0]


def test_team_detail(
    api_client: "APIClient",
    league_factory: "LeagueFactory",
    team_factory: "TeamFactory",
    create_team_data: dict,
) -> None:
    league = league_factory.create()
    create_team_data["league"] = league
    team = team_factory.create(**create_team_data)
    url = reverse("teams-detail", args=[team.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["league"] == league.pk
    assert response.data["name"] == team.name
    assert response.data["city"] == team.city
    assert response.data["number"] == team.number


def test_team_create(
    api_client: "APIClient",
    league_factory: "LeagueFactory",
    create_team_data: dict,
    test_user: "User",
) -> None:
    league = league_factory.create(owner=test_user)
    create_team_data["league"] = league.pk
    url = reverse("teams-list")
    response = api_client.post(url, data=create_team_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED, response
    assert response.data["league"] == create_team_data["league"]
    assert response.data["name"] == create_team_data["name"]
    assert response.data["city"] == create_team_data["city"]
    team = Team.objects.get(name=create_team_data["name"])
    assert team.league == league
    assert team.name == create_team_data["name"]
    assert team.city == create_team_data["city"]


def test_team_update(
    api_client: "APIClient",
    team_factory: "TeamFactory",
    create_team_data: dict,
    test_user: "User",
) -> None:
    create_team_data["league__owner"] = test_user
    team = team_factory.create(**create_team_data)
    url = reverse("teams-detail", args=[team.pk])
    update_data = {"city": "Sosnowiec"}
    response = api_client.patch(url, data=update_data, format="json")
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["city"] == update_data["city"]
    team.refresh_from_db()
    assert team.city == update_data["city"]


def test_team_destroy(
    api_client: "APIClient",
    team_factory: "TeamFactory",
    match_factory: "MatchFactory",
    test_user: "User",
) -> None:
    team = team_factory.create(league__owner=test_user)
    match = match_factory.create(visitor=team)
    url = reverse("teams-detail", args=[team.pk])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response
    with pytest.raises(Team.DoesNotExist):
        Team.objects.get(id=team.pk)
    match.refresh_from_db()
    assert match.visitor is None


def test_team_user_is_not_owner(
    api_client: "APIClient",
    team_factory: "TeamFactory",
) -> None:
    team = team_factory.create()
    url = reverse("teams-detail", args=[team.pk])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response
    response = api_client.patch(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response


def test_team_create_user_is_not_league_owner(
    api_client: "APIClient",
    league_factory: "LeagueFactory",
    create_team_data: dict,
) -> None:
    league = league_factory.create()
    create_team_data["league"] = league.pk
    url = reverse("teams-list")
    response = api_client.post(url, data=create_team_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response
