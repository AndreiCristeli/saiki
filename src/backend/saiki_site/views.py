"""
backend/saiki_site/views.py

Viewing configuration for saiki_site Django's application.
"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from typing import Any
import json


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
    @csrf_exempt
    def request_hint(req) -> JsonResponse:
        if req.method != "POST":
            return JsonResponse({})

        try:
            print(req)
            data = json.loads(req.body)
            name: str = data.get("name")

            print(data, name)

        except:
            name: str = "undef"

        return JsonResponse({
            "msg": name.upper()
        })

    @staticmethod
    def request_entity(req) -> JsonResponse:
        return JsonResponse({
            "name": "Merge Sort",
            "type": "partial",
            "data": {
                "category": ["Sorting", "wrong"],
                "year": [1945, "correct"],
                "average_time_complexity": ["O(n log n)", "correct"],
                "auxiliary_space_complexity": ["O(n)", "partial"],
                "data_structure": ["Array", "correct"],
                "kind_of_solution": ["Exact", "wrong"],
                "generality": ["General-purpose", "wrong"]
            }
        })


class OtherView(object):
    ...

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
