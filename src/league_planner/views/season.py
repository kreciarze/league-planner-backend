from collections import OrderedDict

from django.db.models import Case, F, QuerySet, Value, When
from rest_framework import status
from rest_framework.decorators import action
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

from league_planner.filters import FilterByLeague
from league_planner.models.match import Match
from league_planner.models.season import Season
from league_planner.models.team import Team
from league_planner.pagination import Pagination
from league_planner.permissions import IsLeagueResourceOwner
from league_planner.serializers.season import SeasonSerializer
from league_planner.serializers.team import ScoreboardSerializer


class SeasonViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    permission_classes = (IsAuthenticated, IsLeagueResourceOwner)
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    pagination_class = Pagination
    filterset_class = FilterByLeague

    @action(
        methods=["GET"],
        detail=True,
        url_path="scoreboard",
    )
    def scoreboard(self, request: Request, pk: int) -> Response:
        season = self.get_object()
        teams_queryset = self.teams_queryset(season)
        teams_to_points_map = {team.id: [0, 0] for team in teams_queryset}
        matches_with_points_qs = self.matches_with_points_queryset(season)
        for match in matches_with_points_qs:
            if match.host_id is not None:
                teams_to_points_map[match.host_id][0] += match.host_points
            if match.visitor_id is not None:
                teams_to_points_map[match.visitor_id][1] += match.visitor_points
        scoreboard = []
        for team in teams_queryset:
            points = teams_to_points_map[team.id]
            team.score = points[0] + points[1]
            team.score_as_visitor = points[1]
            scoreboard.append(team)
        scoreboard.sort(key=lambda team: (team.score, team.score_as_visitor), reverse=True)
        data = ScoreboardSerializer(scoreboard, many=True).data
        rest_response_data = OrderedDict(
            count=len(data),
            next=None,
            previous=None,
            results=data,
        )
        return Response(data=rest_response_data, status=status.HTTP_200_OK)

    @staticmethod
    def teams_queryset(season: Season) -> QuerySet:
        return Team.objects.filter(season_id=season.id).all()

    @staticmethod
    def matches_with_points_queryset(season: Season) -> QuerySet:
        return Match.objects.filter(season_id=season.id).annotate(
            host_points=Case(
                When(host_score__gt=F("visitor_score"), then=Value(season.points_per_win)),
                When(host_score=F("visitor_score"), then=Value(season.points_per_draw)),
                default=Value(season.points_per_lose),
            ),
            visitor_points=Case(
                When(visitor_score__gt=F("host_score"), then=Value(season.points_per_win)),
                When(visitor_score=F("host_score"), then=Value(season.points_per_draw)),
                default=Value(season.points_per_lose),
            ),
        )
