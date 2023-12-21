from datetime import datetime

from django.contrib.auth.models import User
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from league_planner.models.league import League
from league_planner.models.match import Match
from league_planner.models.season import Season
from league_planner.models.team import Team


class UserFactory(DjangoModelFactory):
    username = Sequence(lambda n: f"name{n}")
    password = "password"  # noqa: S105

    class Meta:
        model = User
        django_get_or_create = ("username",)


class LeagueFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"league{n}")
    owner = SubFactory(UserFactory)

    class Meta:
        model = League
        django_get_or_create = ("name",)


class SeasonFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"season{n}")
    league = SubFactory(LeagueFactory)

    class Meta:
        model = Season
        django_get_or_create = ("name",)


class TeamFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"team{n}")
    season = SubFactory(SeasonFactory)
    city = "Sosnowiec"

    class Meta:
        model = Team
        django_get_or_create = ("name",)


class MatchFactory(DjangoModelFactory):
    season = SubFactory(SeasonFactory)
    host = SubFactory(TeamFactory)
    visitor = SubFactory(TeamFactory)
    host_score = 20
    visitor_score = 10
    address = "ul. Bogdana Bonera 21/37"
    datetime = datetime.now()

    class Meta:
        model = Match
        django_get_or_create = ("host", "visitor", "datetime", "address")
