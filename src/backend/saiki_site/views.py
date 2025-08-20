"""
backend/saiki_site/views.py

Viewing configuration for saiki_site Django's application.
"""

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from .guesser import guesser, GuessState
from .player_views import PlayerView
from typing import Any
import json


class FrontendView(object):
    """Handles the view of the frontend via the backend."""

    @staticmethod
    @csrf_exempt
    def serve_main_page(req: WSGIRequest) -> HttpResponse:
        """Provides the frontend main page."""

        from os import path

        # inferring the request...
        print(type(req), req)

        # the html source
        index_path: str = path.join(path.dirname(__file__), "../../frontend/site/html/index.html")

        # opening and sending the HTML over
        with open(index_path, encoding="utf-8") as index:
            return HttpResponse(index.read(), content_type="text/html")

    @staticmethod
    @csrf_exempt
    def serve_frontend(req: WSGIRequest) -> HttpResponse:
        if req.user.is_authenticated:
            # print("USER:", req.user, type(req.user))

            # if already authenticated, serves the main-page.
            return FrontendView.serve_main_page(req)

        # else, redirects to the login-page.
        return PlayerView.serve_login(req)

    @staticmethod
    def serve_custom_mode(req: WSGIRequest) -> HttpResponse:
        return render(req, "custom.html")

    @staticmethod
    def serve_daily_mode(req: WSGIRequest) -> HttpResponse:
        return render(req, "index.html")

    @staticmethod
    def serve_tof_mode(req: WSGIRequest) -> HttpResponse:
        return render(req, "trueOrFalse.html")


class GuessView(object):
    """Handles the view of the Guess game mode."""

    @staticmethod
    def empty() -> JsonResponse:
        """Represents an empty JSON response."""
        return JsonResponse({})

    @staticmethod
    @csrf_exempt  # Cookies~
    def request_hint(req: WSGIRequest) -> JsonResponse:
        """Processes the request of a hint, via POST."""

        if req.method != "POST":
            return GuessView.empty()

        try:
            data: dict = json.loads(req.body)
            name: str = data.get("attempt")

            if not isinstance(name, str):
                raise TypeError

        except TypeError | KeyError as e:
            print(e)
            return GuessView.empty()

        guess_state: GuessState = GuessState.from_request(req)
        matches: list[str] = guesser.match_name(guess_state, name)

        return JsonResponse({
            "number_of_matches": len(matches),
            "closest_matches": matches
        })

    @staticmethod
    @csrf_exempt  # Cookies~
    def request_entity(req: WSGIRequest) -> JsonResponse:
        """Processes the request of an entity, via POST."""

        if req.method != "POST":
            return GuessView.empty()

        data: dict[str, Any] = json.loads(req.body)

        try:
            entity: str = data["entity"]

        except KeyError:
            return GuessView.empty()

        # guess_state: GuessState = GuessState.from_request(req)
        # return GuessView.__check_fields(guess_state, entity)
        return GuessState.from_request(req).guess(entity)

    @staticmethod
    @csrf_exempt
    def request_load(req: WSGIRequest) -> JsonResponse:
        """Returns the corresponding data on the cookies, form"""

        if req.method != "POST":
            return GuessView.empty()

        # for instance, ignores the JSON data, as it isn't needed...
        data = json.loads(req.body)

        guess_state: GuessState = GuessState.from_request(req)
        return guess_state.get_collection(data)
