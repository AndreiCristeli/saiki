"""
backend/saiki_site/views.py

Viewing configuration for saiki_site Django's application.
"""

from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .entities import HistoricalEntity
from .guesser import guesser, GuessState
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


# -------------------------------------------------------------------------------------------
from .forms import JogadorForm, JogadorLoginForm
from .models import Jogador
from django.contrib import messages
from django.contrib.auth import login


def jogador_login(request):
    if request.method == "POST":
        form = JogadorLoginForm(request.POST)
        if form.is_valid():
            name_user = form.cleaned_data['name_user']
            password = form.cleaned_data['password']
            try:
                jogador = Jogador.objects.get(name_user=name_user)
                if jogador.check_password(password):
                    login(request, jogador.user)  # o User real associado
                    return redirect('painel_jogador')  # ou outra view pós-login
                else:
                    messages.error(request, "Senha incorreta.")
            except Jogador.DoesNotExist:
                messages.error(request, "Usuário não encontrado.")
    else:
        form = JogadorLoginForm()
    return render(request, "jogador_login.html", {"form": form})


def painel_jogador(request):
    if not request.user.is_authenticated:
        return redirect('jogador_login')

    try:
        jogador = Jogador.objects.get(user=request.user)
    except Jogador.DoesNotExist:
        jogador = None

    return render(request, "painel_jogador.html", {"jogador": jogador})


from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def jogador_create(request):
    if request.method == 'POST':
        form = JogadorForm(request.POST)
        if form.is_valid():
            # Cria o usuário base do Django
            user = User.objects.create_user(
                username=form.cleaned_data['name_user'],
                email=form.cleaned_data['name_email'],
                password=form.cleaned_data['name_password']
            )

            jogador = form.save(commit=False)
            jogador.user = user  # associa o usuário criado
            jogador.set_password(form.cleaned_data['name_password'])  # hash na senha
            jogador.save()

            return redirect('jogador_success')  # ou a tela que desejar
    else:
        form = JogadorForm()

    return render(request, 'jogador_form.html', {'form': form})


def jogador_success(request):
    return HttpResponse("Jogador criado com sucesso!")
