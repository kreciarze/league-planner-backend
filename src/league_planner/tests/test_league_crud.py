import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from league_planner.models.league import League
from league_planner.models.match import Match
from league_planner.models.team import Team
from league_planner.tests.factories import LeagueFactory, MatchFactory, SeasonFactory, TeamFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def create_league_data() -> dict:
    return {
        "name": "NBA",
    }


def test_leagues_list(
    api_client: APIClient,
    league_factory: LeagueFactory,
) -> None:
    url = reverse("leagues-list")
    league = league_factory.create(name="league0")
    for i in range(1, 10):
        league_factory.create(name=f"league{i}")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["results"][0]["owner_login"] == league.owner.username
    assert response.data["count"] == 10


def test_league_detail(
    api_client: APIClient,
    league_factory: LeagueFactory,
) -> None:
    league = league_factory.create(name="NBA")
    url = reverse("leagues-detail", args=[league.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["name"] == league.name
    assert response.data["owner"] == league.owner.pk


def test_league_create(
    api_client: APIClient,
    test_user: User,
    create_league_data: dict,
) -> None:
    url = reverse("leagues-list")
    response = api_client.post(url, data=create_league_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED, response
    assert response.data["name"] == create_league_data["name"]
    assert response.data["owner"] == test_user.pk
    league = League.objects.get(name=create_league_data["name"])
    assert league.name == create_league_data["name"]
    assert league.owner == test_user


def test_league_update(
    api_client: APIClient,
    league_factory: LeagueFactory,
    create_league_data: dict,
    test_user: User,
) -> None:
    create_league_data["owner"] = test_user
    league = league_factory.create(**create_league_data)
    url = reverse("leagues-detail", args=[league.pk])
    update_data = {"name": "WNBA"}
    response = api_client.patch(url, data=update_data, format="json")
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["name"] == update_data["name"]
    league.refresh_from_db()
    assert league.name == update_data["name"]


def test_league_destroy(
    api_client: APIClient,
    league_factory: LeagueFactory,
    season_factory: SeasonFactory,
    team_factory: TeamFactory,
    match_factory: MatchFactory,
    test_user: User,
) -> None:
    league = league_factory.create(owner=test_user)
    season = season_factory.create(league=league)
    team = team_factory.create(season=season)
    match = match_factory.create(season=season, host=team)
    url = reverse("leagues-detail", args=[league.pk])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response
    with pytest.raises(League.DoesNotExist):
        League.objects.get(id=league.pk)
    with pytest.raises(Team.DoesNotExist):
        Team.objects.get(id=team.pk)
    with pytest.raises(Match.DoesNotExist):
        Match.objects.get(id=match.pk)


def test_league_user_is_not_owner(
    api_client: APIClient,
    league_factory: LeagueFactory,
) -> None:
    league = league_factory.create()
    url = reverse("leagues-detail", args=[league.pk])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response
    response = api_client.patch(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response
