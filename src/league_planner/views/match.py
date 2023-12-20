from rest_framework import viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated

from league_planner.filters import FilterByLeague
from league_planner.models.match import Match
from league_planner.pagination import Pagination
from league_planner.permissions import IsLeagueResourceOwner
from league_planner.serializers.match import MatchDetailSerializer, MatchSerializer


class MatchViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    permission_classes = (IsAuthenticated, IsLeagueResourceOwner)
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    pagination_class = Pagination
    filterset_class = FilterByLeague

    def get_serializer_class(self) -> type[MatchSerializer]:
        if self.action in ["list", "retrieve"]:
            return MatchDetailSerializer
        return MatchSerializer
