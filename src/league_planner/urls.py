from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from league_planner.views.league import LeagueViewSet
from league_planner.views.match import MatchViewSet
from league_planner.views.team import TeamViewSet
from league_planner.views.user import CreateUserView, LoginView

router = SimpleRouter()
router.register("leagues", LeagueViewSet, "leagues")
router.register("teams", TeamViewSet, "teams")
router.register("matches", MatchViewSet, "matches")
router.register("register", CreateUserView, "register")


urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view()),
]
