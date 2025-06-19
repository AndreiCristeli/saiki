"""
backend/saiki_site/views.py

Viewing configuration for saiki_site Django's application.
"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def serve_frontend(_) -> HttpResponse:
    from os import path

    index_path: str = path.join(path.dirname(__file__), "../../frontend/site/html/index.html")
    with open(index_path, encoding="utf-8") as index:
        return HttpResponse(index.read(), content_type="text/html")


def read_root(request) -> JsonResponse:
    print(request)

    return JsonResponse(
        {
            "msg": "Hello from backend! Camarada"
        }
    )


def read_root1(request) -> JsonResponse:
    print(request)

    return JsonResponse(
        {
            "msg": "Helicóptero"
        }
    )
