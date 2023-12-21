from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from league_planner.models.league import League
from league_planner.models.resource_with_owner import ResourceWithOwner
from league_planner.models.season import Season


class IsLeagueOwner(permissions.BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: GenericViewSet,
        model: ResourceWithOwner,
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return model.is_owner(request.user)


class IsLeagueResourceOwner(IsLeagueOwner):
    def has_permission(
        self,
        request: Request,
        view: GenericViewSet,
    ) -> bool:
        if request.method != "POST":
            return True

        league_id = request.data.get("league")
        if not league_id:
            return True

        try:
            league = League.objects.get(id=league_id)
            return league.is_owner(request.user)
        except League.DoesNotExist:
            return True


class IsSeasonResourceOwner(IsLeagueOwner):
    def has_permission(
        self,
        request: Request,
        view: GenericViewSet,
    ) -> bool:
        if request.method != "POST":
            return True

        season_id = request.data.get("season")
        if not season_id:
            return True

        try:
            season = Season.objects.get(id=season_id)
            return season.is_owner(request.user)
        except Season.DoesNotExist:
            return True
