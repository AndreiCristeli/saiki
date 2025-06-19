"""
backend/saiki_site/views.py

Viewing configuration for saiki_site Django's application.
"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from typing import Any
import json
from .models import example_algorithm


class FrontendView(object):
    """Handles the view of the frontend via the backend."""

    @staticmethod
    def serve_frontend(req) -> HttpResponse:
        """Provides the frontend main page.

            @TODO: This method can and may have variations concerning the different web pages."""

        from os import path

        # inferring the request...
        print(type(req), req)

        # the html source
        index_path: str = path.join(path.dirname(__file__), "../../frontend/site/html/index.html")

        # opening and sending the HTML over
        with open(index_path, encoding="utf-8") as index:
            return HttpResponse(index.read(), content_type="text/html")


class GuessView(object):
    """Handles the view of the Guess game mode."""

    @staticmethod
    @csrf_exempt    # Cookies~
    def request_hint(req) -> JsonResponse:
        """Processes the request of a hint, via POST."""

        if req.method != "POST":
            # empty return~
            return JsonResponse({})
        
        try:
            data = json.loads(req.body)
            name: str = data.get("attempt")

            if not isinstance(name, str):
                raise TypeError

        except TypeError | KeyError as e:
            name: str = "undef"
            print(e)

        return JsonResponse({
            "name": name.upper()
        })

    @staticmethod
    @csrf_exempt    # Cookies~
    def request_entity(req) -> JsonResponse:
        """Processes the request of an entity, via POST."""

        print(type(req))

        if req.method != "POST":
            # empty return~
            return JsonResponse({})

        try:
            data = json.loads(req.body)
            entity: str = data.get("entity")

        except:
            return JsonResponse({})
        
        if entity != "merge sort":
            return JsonResponse({})

        # Mocking gathering the data~
        # return JsonResponse({})
        return example_algorithm.to_json()


class OtherView(object):

    @staticmethod
    def read_root(req) -> JsonResponse:
        return JsonResponse(
            {
                "msg": "Hello from backend! Camarada"
            }
        )


def read_root1(req) -> JsonResponse:
    return JsonResponse(
        {
            "msg": "Helicóptero"
        }
    )
