import pytest
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from league_planner.models.team import Team
from league_planner.tests.factories import LeagueFactory, MatchFactory, SeasonFactory, TeamFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def create_team_data() -> dict:
    return {"name": "RKS Chuwdu", "city": "Kurwix"}


def test_teams_list(
    api_client: APIClient,
    season_factory: SeasonFactory,
    team_factory: TeamFactory,
) -> None:
    url = reverse("teams-list")
    season = season_factory.create()
    for i in range(10):
        team_factory.create(
            name=f"team{i}",
            season=season,
        )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["count"] == 10


def test_teams_filtering(
    api_client: APIClient,
    season_factory: SeasonFactory,
    team_factory: TeamFactory,
) -> None:
    url = reverse("teams-list")
    season1 = season_factory.create(name="NBA")
    season2 = season_factory.create(name="WNBA")
    for i in range(5):
        team_factory.create(
            name=f"NBA team{i}",
            season=season1,
        )
    for i in range(5):
        team_factory.create(
            name=f"WNBA team{i}",
            season=season2,
        )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["count"] == 10
    response = api_client.get(f"{url}?season={season1.pk}")
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["count"] == 5
    assert response.data["results"][0]["season"] == model_to_dict(season1)
    assert response.data["results"][0]["name"] is not None
    assert response.data["results"][0]["city"] is not None
    assert response.data["results"][0]["number"] is None
    assert "image" not in response.data["results"][0]


def test_team_detail(
    api_client: APIClient,
    season_factory: SeasonFactory,
    team_factory: TeamFactory,
    create_team_data: dict,
) -> None:
    season = season_factory.create()
    create_team_data["season"] = season
    team = team_factory.create(**create_team_data)
    url = reverse("teams-detail", args=[team.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["season"] == model_to_dict(season)
    assert response.data["name"] == team.name
    assert response.data["city"] == team.city
    assert response.data["number"] == team.number


def test_team_create(
    api_client: APIClient,
    season_factory: SeasonFactory,
    create_team_data: dict,
    test_user: User,
) -> None:
    season = season_factory.create(league__owner=test_user)
    create_team_data["season"] = season.pk
    url = reverse("teams-list")
    response = api_client.post(url, data=create_team_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED, response
    assert response.data["season"] == create_team_data["season"]
    assert response.data["name"] == create_team_data["name"]
    assert response.data["city"] == create_team_data["city"]
    team = Team.objects.get(name=create_team_data["name"])
    assert team.season == season
    assert team.name == create_team_data["name"]
    assert team.city == create_team_data["city"]


def test_team_update(
    api_client: APIClient,
    team_factory: TeamFactory,
    create_team_data: dict,
    test_user: User,
) -> None:
    create_team_data["season__league__owner"] = test_user
    team = team_factory.create(**create_team_data)
    url = reverse("teams-detail", args=[team.pk])
    update_data = {"city": "Sosnowiec"}
    response = api_client.patch(url, data=update_data, format="json")
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["city"] == update_data["city"]
    team.refresh_from_db()
    assert team.city == update_data["city"]


def test_team_destroy(
    api_client: APIClient,
    team_factory: TeamFactory,
    match_factory: MatchFactory,
    test_user: User,
) -> None:
    team = team_factory.create(season__league__owner=test_user)
    match = match_factory.create(visitor=team)
    url = reverse("teams-detail", args=[team.pk])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response
    with pytest.raises(Team.DoesNotExist):
        Team.objects.get(id=team.pk)
    match.refresh_from_db()
    assert match.visitor is None


def test_team_user_is_not_owner(
    api_client: APIClient,
    team_factory: TeamFactory,
) -> None:
    team = team_factory.create()
    url = reverse("teams-detail", args=[team.pk])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response
    response = api_client.patch(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response


def test_team_create_user_is_not_league_owner(
    api_client: APIClient,
    league_factory: LeagueFactory,
    season_factory: SeasonFactory,
    create_team_data: dict,
) -> None:
    league = league_factory.create()
    season = season_factory.create(league=league)
    create_team_data["season"] = season.pk
    url = reverse("teams-list")
    response = api_client.post(url, data=create_team_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response
