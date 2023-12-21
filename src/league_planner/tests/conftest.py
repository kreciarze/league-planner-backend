from typing import Generator

import pytest
from django.contrib.auth.models import User
from pytest_django.fixtures import SettingsWrapper
from pytest_django.lazy_django import skip_if_no_django
from pytest_factoryboy import register
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .factories import LeagueFactory, MatchFactory, SeasonFactory, TeamFactory, UserFactory

pytestmark = [pytest.mark.django_db]


register(UserFactory)
register(LeagueFactory)
register(SeasonFactory)
register(TeamFactory)
register(MatchFactory)


@pytest.fixture(scope="session")
def session_settings() -> "Generator":
    skip_if_no_django()
    wrapper = SettingsWrapper()
    yield wrapper
    wrapper.finalize()


@pytest.fixture()
def test_user(user_factory: "UserFactory") -> "User":
    return user_factory.create(username="test", password="test")  # noqa: S105, S106


@pytest.fixture()
def test_token(test_user: "User") -> "Token":
    return Token.objects.create(user=test_user)


@pytest.fixture()
def api_client(
    test_token: "Token",
) -> "APIClient":
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + test_token.key)
    return client
