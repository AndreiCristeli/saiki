"""
backend/saiki_site/views.py

Viewing configuration for saiki_site Django's application.
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
<<<<<<< Updated upstream
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
=======
from django.views.decorators.csrf import csrf_exempt
from .forms import CriarSessaoForm
from .guesser import guesser, GuessState
>>>>>>> Stashed changes
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



#-------------------------------------------------------------------------------------------
from .forms import JogadorForm, JogadorLoginForm, MessageForm
from .models import Jogador, Session, message, chat
from django.contrib import messages
from django.contrib.auth import login
from django.utils import timezone
import time


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

from .models import Session, Jogador, Jogo_daily, Jogo_custom, Jogo_VF

def criar_sessao(request):
    if not request.user.is_authenticated:
        return redirect('login')

    jogador = Jogador.objects.get(user=request.user)

    if request.method == 'POST':
        tipo = request.POST.get('tipo_jogo')  # vem direto do painel

        # Gera chave única
        timestamp = int(time.time())
        public_key = f"{jogador.name_user}_{timestamp}"

        # Cria a sessão
        sessao = Session.objects.create(
            public_key=public_key,
            root_player=jogador,
        )

        # Cria o jogo correspondente
        if tipo == 'daily':
            jogo = Jogo_daily.objects.create(session=sessao)
        elif tipo == 'custom':
            jogo = Jogo_custom.objects.create(session=sessao)
        elif tipo == 'vf':
            jogo = Jogo_VF.objects.create(session=sessao)
        else:
            jogo = None

        if jogo:
            jogo.players.add(jogador)

        return redirect('ver_sessao', sessao_id=sessao.id)

from django.shortcuts import render, get_object_or_404, redirect
from .forms import MessageForm, JogoDailyForm2
from django.http import JsonResponse
from django.db.models import F

from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def registrar_tentativa(request, sessao_id):
    """
    Dá +1 em tentativas do Jogo_daily ligado à Session(sessao_id) e devolve o número novo.
    ATÔMICO e sem depender de nada além do ID da sessão.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    updated = Jogo_daily.objects.filter(session_id=sessao_id).update(tentativas=F('tentativas') + 1)
    if not updated:
        # não existia jogo_daily ainda — cria com tentativas=1
        jogo = Jogo_daily.objects.create(session_id=sessao_id, tentativas=1)
        return JsonResponse({ "tentativas": jogo.tentativas })

    # pega o valor atualizado sem race condition
    novo_valor = Jogo_daily.objects.filter(session_id=sessao_id).values_list('tentativas', flat=True).get()
    return JsonResponse({ "tentativas": novo_valor })



def ver_sessao(request, sessao_id):
    if not request.user.is_authenticated:
        return redirect('login')

    jogador = get_object_or_404(Jogador, user=request.user)
    sessao = get_object_or_404(Session, id=sessao_id)

    # Pega o jogo diário (se existir)
    jogo_daily = None
    tentativas = 0
    try:
        jogo_daily = Jogo_daily.objects.get(session=sessao)
        tentativas = jogo_daily.tentativas
    except Jogo_daily.DoesNotExist:
        pass

    if request.method == 'POST':
        # Chat
        if 'texto' in request.POST:
            form = MessageForm(request.POST)
            if form.is_valid() and sessao.status:
                texto = form.cleaned_data['texto']
                nova_msg = message.objects.create(sender=jogador, texto=texto)
                destinatarios = sessao.players.all()
                nova_msg.receivers.set(destinatarios)
                nova_msg.save()
                sessao.chat.add_message(nova_msg)
                sessao.chat.participants.add(*destinatarios)
                return redirect('ver_sessao', sessao_id=sessao.id)
    else:
        form = MessageForm()

    tempo_corrente = timezone.now() - sessao.data_inicio if sessao.status else sessao.session_time
    mensagens = sessao.chat.messages.order_by('timestamp')

    # Descobre tipo de jogo
    tipo_jogo = "Não definido"
    template = 'sessao.html'
    if jogo_daily:
        tipo_jogo = "Diário"
        template = 'jogo_daily.html'
    elif sessao.games.filter(jogo_custom__isnull=False).exists():
        tipo_jogo = "Customizado"
    elif sessao.games.filter(jogo_vf__isnull=False).exists():
        tipo_jogo = "Verdadeiro/Falso"

    return render(request, template, {
        'sessao': sessao,
        'jogador': jogador,
        'mensagens': mensagens,
        'tempo_corrente': tempo_corrente,
        'form': form,
        'jogo_form': jogo_daily,   # objeto inteiro (caso precise acessar mais coisas)
        'tentativas': tentativas,  # contador já resolvido
        'tipo_jogo': tipo_jogo,
    })

    
def encerrar_sessao(request, sessao_id):
    if not request.user.is_authenticated:
        return redirect('login')

    sessao = get_object_or_404(Session, id=sessao_id)
    if request.user == sessao.root_player.user:
        sessao.end_session()

    return redirect('ver_sessao', sessao_id=sessao_id)

def entrar_sessao(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        chave = request.POST.get('chave_publica')
        jogador = Jogador.objects.get(user=request.user)

        try:
            sessao = Session.objects.get(public_key=chave, status=True)
        except Session.DoesNotExist:
            messages.error(request, "Sessão não encontrada ou inativa.")
            return redirect('painel_jogador')

        # Adiciona o jogador à sessão e ao chat se ainda não estiver
        if jogador not in sessao.players.all():
            sessao.players.add(jogador)
        if jogador not in sessao.active_players.all():
            sessao.active_players.add(jogador)
        if jogador not in sessao.chat.participants.all():
            sessao.chat.participants.add(jogador)

        return redirect('ver_sessao', sessao_id=sessao.id)

<<<<<<< Updated upstream
    return redirect('painel_jogador')
=======
    return redirect('painel_jogador')


from django.http import JsonResponse

>>>>>>> Stashed changes
