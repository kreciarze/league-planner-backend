from typing import Any

from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from league_planner.models.league import League


class IsLeagueOwner(permissions.BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: GenericViewSet,
        league: League,
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return self.is_owner(request.user, league)

    @staticmethod
    def is_owner(user: User, league: League) -> bool:
        return user == league.owner


class IsLeagueResourceOwner(IsLeagueOwner):
    @staticmethod
    def is_owner(user: User, obj: Any) -> bool:
        return user == obj.league.owner

    def has_permission(
        self,
        request: Request,
        view: GenericViewSet,
    ) -> bool:
        if request.method == "POST":
            try:
                league = League.objects.get(id=request.data.get("league"))
            except League.DoesNotExist:
                league = view.get_object().league

            if request.user != league.owner:
                return False
        return super().has_permission(request, view)
