"""
backend/saiki_site/urls.py

URL configuration for saiki_site Django's application.
"""

from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver
from . import views


urlpatterns: list[URLPattern | URLResolver] = [

    # Frontend views.
    path("", views.FrontendView.serve_frontend, name="main"),
    path("custom/", views.FrontendView.serve_custom_mode, name="custom"),
    path("daily/", views.FrontendView.serve_daily_mode, name="daily"),
    path("tof/", views.FrontendView.serve_tof_mode, name="tof"),

    # Guess mode requests.
    path("api/guess/hint/", views.GuessView.request_hint),
    path("api/guess/entity/", views.GuessView.request_entity),
    path("api/guess/load/", views.GuessView.request_load),
    
    # ToF mode requests.
    path("api/true-or-false/start/", views.TrueOrFalseView.start_game),
    path("api/true-or-false/answer/", views.TrueOrFalseView.submit_answer),

    # Player urls.
    path("login/", views.PlayerView.serve_login, name="player-login"),
    path("logout/", views.PlayerView.logout, name="player-logout"),

    path("player/new/", views.PlayerView.player_create, name="player-create"),
    path("player/register/", views.PlayerView.player_create, name="player-register"),
    path("player/success/", views.PlayerView.player_success, name="player-success"),
    path("player/panel/", views.PlayerView.player_panel, name="player-panel"),

    # Sessions.
    path("criar-sessao/", views.PlayerView.session_create, name="session-create"),
    path("session/<int:sessao_id>/", views.PlayerView.session_view, name="session-view"),
    path("session/<int:sessao_id>/encerrar/", views.PlayerView.session_end, name="session-end"),
    path("entrar-sessao/", views.PlayerView.session_join, name="session-join"),
]
