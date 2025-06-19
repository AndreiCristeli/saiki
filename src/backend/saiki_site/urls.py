"""
backend/saiki_site/urls.py

URL configuration for saiki_site Django's application.
"""

from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver
from . import views


urlpatterns: list[URLPattern | URLResolver] = [
    path("", views.serve_frontend),

    path("api/cmrd/", views.read_root),
    path("api/hangar/", views.read_root1),
]
