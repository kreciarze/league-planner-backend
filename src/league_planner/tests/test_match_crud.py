from datetime import datetime, timedelta

import pytest
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from league_planner import settings
from league_planner.models.match import Match
from league_planner.tests.factories import LeagueFactory, MatchFactory, SeasonFactory, TeamFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def create_match_data() -> dict:
    match_datetime = datetime.now() + timedelta(days=2)
    return {
        "host_score": 21,
        "visitor_score": 37,
        "address": "ul. Bogdana Bonera 21/37",
        "datetime": match_datetime.strftime(settings.FE_DATETIME_FORMAT),
    }


def test_matches_list(
    api_client: APIClient,
    season_factory: SeasonFactory,
    team_factory: TeamFactory,
    match_factory: MatchFactory,
) -> None:
    url = reverse("matches-list")
    season = season_factory.create()
    host = team_factory.create()
    visitor = team_factory.create()
    for i in range(10):
        match_factory.create(
            season=season,
            host=host,
            visitor=visitor,
            address=f"address {i}",
        )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["count"] == 10


def test_match_detail(
    api_client: APIClient,
    season_factory: SeasonFactory,
    team_factory: TeamFactory,
    match_factory: MatchFactory,
    create_match_data: dict,
) -> None:
    season = season_factory.create()
    host = team_factory.create(season=season)
    visitor = team_factory.create(season=season)
    create_match_data["season"] = season
    create_match_data["host"] = host
    create_match_data["visitor"] = visitor
    match = match_factory.create(**create_match_data)
    url = reverse("matches-detail", args=[match.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["season"] == season.pk
    assert response.data["host"] == model_to_dict(host, exclude=["image"])
    assert response.data["visitor"] == model_to_dict(visitor, exclude=["image"])
    assert response.data["host_score"] == create_match_data["host_score"]
    assert response.data["visitor_score"] == create_match_data["visitor_score"]
    assert response.data["address"] == create_match_data["address"]
    assert response.data["datetime"] == create_match_data["datetime"].replace("T", " ")


def test_match_create(
    api_client: APIClient,
    season_factory: SeasonFactory,
    team_factory: TeamFactory,
    create_match_data: dict,
    test_user: User,
) -> None:
    season = season_factory.create(league__owner=test_user)
    host = team_factory.create(season=season)
    visitor = team_factory.create(season=season)
    create_match_data["season"] = season.pk
    create_match_data["host"] = host.pk
    create_match_data["visitor"] = visitor.pk
    url = reverse("matches-list")
    response = api_client.post(url, data=create_match_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED, response
    assert response.data["season"] == season.pk
    assert response.data["host"] == host.pk
    assert response.data["visitor"] == visitor.pk
    assert response.data["host_score"] == create_match_data["host_score"]
    assert response.data["visitor_score"] == create_match_data["visitor_score"]
    assert response.data["address"] == create_match_data["address"]
    assert response.data["datetime"] == create_match_data["datetime"].replace("T", " ")
    match = Match.objects.get(host=host, visitor=visitor)
    assert match.season == season
    assert match.host == host
    assert match.visitor == visitor
    assert match.host_score == create_match_data["host_score"]
    assert match.visitor_score == create_match_data["visitor_score"]
    assert match.address == create_match_data["address"]
    assert match.datetime.strftime(settings.FE_DATETIME_FORMAT) == create_match_data["datetime"]


def test_match_update(
    api_client: APIClient,
    season_factory: SeasonFactory,
    team_factory: TeamFactory,
    match_factory: MatchFactory,
    create_match_data: dict,
    test_user: User,
) -> None:
    season = season_factory.create(league__owner=test_user)
    host = team_factory.create(season=season)
    visitor = team_factory.create(season=season)
    create_match_data["season"] = season
    create_match_data["host"] = host
    create_match_data["visitor"] = visitor
    match = match_factory.create(**create_match_data)
    url = reverse("matches-detail", args=[match.pk])
    update_data = {"host_score": None, "visitor_score": None}
    response = api_client.patch(url, data=update_data, format="json")
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["season"] == season.pk
    assert response.data["host"] == host.pk
    assert response.data["visitor"] == visitor.pk
    assert response.data["host_score"] == update_data["host_score"]
    assert response.data["visitor_score"] == update_data["visitor_score"]
    match.refresh_from_db()
    assert match.season == season
    assert match.host == host
    assert match.visitor == visitor
    assert match.host_score == update_data["host_score"]
    assert match.visitor_score == update_data["visitor_score"]


def test_match_destroy(
    api_client: APIClient,
    match_factory: MatchFactory,
    test_user: User,
) -> None:
    match = match_factory.create(season__league__owner=test_user)
    url = reverse("matches-detail", args=[match.pk])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response
    with pytest.raises(Match.DoesNotExist):
        Match.objects.get(id=match.pk)


def test_match_user_is_not_owner(
    api_client: APIClient,
    match_factory: MatchFactory,
) -> None:
    match = match_factory.create()
    url = reverse("matches-detail", args=[match.pk])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response
    response = api_client.patch(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response


def test_match_create_user_is_not_league_owner(
    api_client: APIClient,
    league_factory: LeagueFactory,
    season_factory: SeasonFactory,
    create_match_data: dict,
) -> None:
    league = league_factory.create()
    season = season_factory.create(league=league)
    create_match_data["season"] = season.pk
    url = reverse("teams-list")
    response = api_client.post(url, data=create_match_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response
