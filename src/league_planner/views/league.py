from typing import Any

from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from league_planner.models.league import League
from league_planner.pagination import Pagination
from league_planner.permissions import IsLeagueOwner
from league_planner.serializers.league import LeagueSerializer


class LeagueViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    permission_classes = (IsAuthenticated, IsLeagueOwner)
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    pagination_class = Pagination

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request.data["owner"] = request.user.pk
        return super().create(request, *args, **kwargs)
