"""
backend/saiki_site/urls.py

URL configuration for saiki_site Django's application.
"""

from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver
from . import views


urlpatterns: list[URLPattern | URLResolver] = [
    path("", views.FrontendView.serve_frontend),

    # Testing
    path("api/cmrd/", views.OtherView.read_root),
    path("api/hangar/", views.read_root1),

    # Guess mode requests
    path("api/guess/hint/", views.GuessView.request_hint),
    path("api/guess/entity/", views.GuessView.request_entity),
]
