"""
backend/saiki_site/player_views.py

...
"""

from django.contrib.auth import logout
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import Form

from .forms import JogadorForm, JogadorLoginForm, MessageForm
from .models import Jogador, Session, message
from django.contrib import messages
from django.contrib.auth import login
from django.utils import timezone
from django.contrib.auth.models import User

import time


class PlayerView(object):

    @staticmethod
    def __authenticate_user(username: str, password: str) -> None | Jogador:
        """Handles the user authentication."""

        try:
            player: Jogador = Jogador.objects.get(name_user=username)

            if player.check_password(password):
                return player

            return None

        except Jogador.DoesNotExist:
            return None

    @staticmethod
    @csrf_exempt
    def serve_login(req: WSGIRequest) -> HttpResponse:
        """Serves the login-page to the request."""

        if req.method == "POST":
            form: Form = JogadorLoginForm(req.POST)

            if form.is_valid():
                name_user = form.cleaned_data["name_user"]
                password = form.cleaned_data["password"]

                player: None | Jogador = PlayerView.__authenticate_user(name_user, password)
                if player:
                    login(req, player.user)
                    req.session["doidera"] = 1

                    return PlayerView.serve_logged(req)

                messages.error(req, "Usuário não encontrado.")

        else:
            # req.session["cala_a_boca"] = 2

            try:
                # print("cala a boca:", req.session["cala_a_boca"])
                # print(req.session.load())
                ...

            except KeyError:
                ...
            form = JogadorLoginForm()

        return render(req, "player_login.html", {"form": form})

    @staticmethod
    @csrf_exempt
    def serve_logged(req: WSGIRequest) -> HttpResponse:
        return redirect("player-panel")

    @staticmethod
    @csrf_exempt
    def logout(req: WSGIRequest) -> HttpResponse:
        """Handles the logout of the user.
        De-authenticates it and then servers the login-page."""

        logout(req)
        return PlayerView.serve_login(req)

    @staticmethod
    @csrf_exempt
    def player_panel(req: WSGIRequest) -> HttpResponse:
        if not req.user.is_authenticated:
            return redirect("player-login")

        try:
            jogador: Jogador | None = Jogador.objects.get(user=req.user)

        except Jogador.DoesNotExist:
            jogador = None

        return render(req, "player_panel.html", {"jogador": jogador})

    @staticmethod
    def player_create(request) -> HttpResponse:
        if request.method == "POST":
            form = JogadorForm(request.POST)

            if form.is_valid():

                # Cria o usuário base do Django
                user = User.objects.create_user(
                    username=form.cleaned_data["name_user"],
                    email=form.cleaned_data["name_email"],
                    password=form.cleaned_data["name_password"]
                )

                jogador = form.save(commit=False)
                jogador.user = user  # associa o usuário criado
                jogador.set_password(form.cleaned_data["name_password"])  # hash na senha
                jogador.save()

                return redirect("player-success")  # ou a tela que desejar
        else:
            form = JogadorForm()

        return render(request, "player_form.html", {"form": form})

    @staticmethod
    def player_success(req: WSGIRequest) -> HttpResponse:
        # return HttpResponse("Jogador criado com sucesso!")

        return PlayerView.serve_logged(req)
    
    @staticmethod
    def session_create(request) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect("login")  # ou outra view

        jogador = Jogador.objects.get(user=request.user)

        # Gera chave única com name_user + timestamp
        timestamp = int(time.time())
        public_key = f"{jogador.name_user}_{timestamp}"
        print("public key:", public_key)

        # Cria a sessão (chat será criado automaticamente no save())
        sessao = Session.objects.create(
            public_key=public_key,
            root_player=jogador,
        )

        return redirect("session-view", sessao_id=sessao.id)

    @staticmethod
    def session_view(request, sessao_id):
        if not request.user.is_authenticated:
            return redirect("login")

        jogador = Jogador.objects.get(user=request.user)
        sessao = get_object_or_404(Session, id=sessao_id)

        if request.method == "POST":
            form = MessageForm(request.POST)
            if form.is_valid() and sessao.status:
                texto = form.cleaned_data["texto"]

                # Cria a mensagem com o remetente
                nova_msg = message.objects.create(sender=jogador, texto=texto)

                # Define todos com acesso ao chat como destinatários, incluindo o próprio sender
                destinatarios = sessao.players.all()  # ou: sessao.chat.participants.all() se preferir
                nova_msg.receivers.set(destinatarios)
                nova_msg.save()

                # Adiciona a mensagem ao chat
                sessao.chat.add_message(nova_msg)

                # Garante que todos os jogadores estejam nos participantes do chat
                sessao.chat.participants.add(*destinatarios)

                return redirect("session-view", sessao_id=sessao.id)

        else:
            form = MessageForm()

        tempo_corrente = timezone.now() - sessao.data_inicio if sessao.status else sessao.session_time
        mensagens = sessao.chat.messages.order_by("timestamp")

        return render(request, "session.html", {
            "sessao": sessao,
            "jogador": jogador,
            "mensagens": mensagens,
            "tempo_corrente": tempo_corrente,
            "form": form,
        })

    @staticmethod
    def session_end(request, sessao_id):
        if not request.user.is_authenticated:
            return redirect("login")

        sessao = get_object_or_404(Session, id=sessao_id)
        if request.user == sessao.root_player.user:
            sessao.end_session()

        return redirect("session-view", sessao_id=sessao_id)

    @staticmethod
    def session_join(request):
        if not request.user.is_authenticated:
            return redirect("login")

        if request.method == "POST":
            chave = request.POST.get("chave_publica")
            jogador = Jogador.objects.get(user=request.user)

            try:
                sessao = Session.objects.get(public_key=chave, status=True)

            except Session.DoesNotExist:
                messages.error(request, "Sessão não encontrada ou inativa.")
                return redirect("player-panel")

            # Adiciona o jogador à sessão e ao chat se ainda não estiver
            if jogador not in sessao.players.all():
                sessao.players.add(jogador)
            if jogador not in sessao.active_players.all():
                sessao.active_players.add(jogador)
            if jogador not in sessao.chat.participants.all():
                sessao.chat.participants.add(jogador)

            return redirect("session-view", sessao_id=sessao.id)

        return redirect("player-panel")
