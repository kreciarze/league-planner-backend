from django.db.models.query import QuerySet
from django_filters.rest_framework import BaseInFilter, FilterSet


class SeasonIdFilter(BaseInFilter):
    def filter(self, qs: QuerySet, ids: list[int]) -> QuerySet:  # noqa: A003
        return qs.filter(season__in=ids) if ids else qs


class LeagueIdFilter(BaseInFilter):
    def filter(self, qs: QuerySet, ids: list[int]) -> QuerySet:  # noqa: A003
        return qs.filter(league__in=ids) if ids else qs


class FilterBySeason(FilterSet):
    season = SeasonIdFilter(lookup_expr="exact")


class FilterByLeague(FilterSet):
    league = LeagueIdFilter(lookup_expr="exact")
