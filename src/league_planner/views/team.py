from django.http import HttpResponse
from rest_framework import status, viewsets
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

from league_planner.filters import FilterByLeague
from league_planner.models.team import Team
from league_planner.pagination import Pagination
from league_planner.permissions import IsLeagueResourceOwner
from league_planner.serializers.team import TeamImageSerializer, TeamSerializer


class TeamViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    permission_classes = (IsAuthenticated, IsLeagueResourceOwner)
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = Pagination
    filterset_class = FilterByLeague

    @action(
        methods=["POST"],
        detail=True,
        url_path="image-upload",
        url_name="image_upload",
        serializer_class=TeamImageSerializer,
    )
    def image_upload(self, request: Request, pk: int) -> Response:
        team = self.get_object()
        serializer = self.get_serializer(team, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["GET"],
        detail=True,
        url_path="image",
        url_name="image",
    )
    def image_download(self, request: Request, pk: int) -> Response | HttpResponse:
        team = self.get_object()
        try:
            image = team.image.read()
        except ValueError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return HttpResponse(image, content_type="image/png")

    @action(
        methods=["DELETE"],
        detail=True,
        url_path="image-delete",
        url_name="image_delete",
    )
    def image_delete(self, request: Request, pk: int) -> Response:
        team = self.get_object()
        team.image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
