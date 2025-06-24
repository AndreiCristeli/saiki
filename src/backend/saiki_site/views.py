"""
backend/saiki_site/views.py

Viewing configuration for saiki_site Django's application.
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
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
    def check_fields(selected_entity: int | None, entity_name: str) -> JsonResponse:
        """Checks if the entity is in the"""

        from random import randint

        with open("src/frontend/site/scripts/test.json", "r", encoding="utf-8") as file:
            json_stream = json.load(file)

        print(type(json_stream))

        if selected_entity is None:
            # choosing an entity
            from random import randint
            selected_entity: int = randint(0, len(json_stream) - 1)

        correct_entity = json_stream[selected_entity]

        for entity in json_stream:
            # @TODO: to abstract and improve comparison!
            if entity["name"].lower() == entity_name:

                response: dict = {
                    "name": entity["name"],
                    "data": {},
                    "type": "correct"
                }

                for field in entity["data"]:
                    guess_type: str = "correct" if entity["data"][field] == correct_entity["data"][field] else "wrong"
                    response["data"][field] = [entity["data"][field], guess_type]

                    if response["type"] == "correct":
                        response["type"] = guess_type

                response_json: JsonResponse = JsonResponse(response)

                if response["type"] == "correct":
                    response_json.delete_cookie("selected")
                else:
                    response_json.set_cookie("selected", selected_entity)

                return response_json

        response_json: JsonResponse = JsonResponse({})
        response_json.set_cookie("selected", selected_entity)
        return response_json

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

        # Mocking gathering the data~
        # return JsonResponse({})
        # return example_algorithm.to_json()
        print(entity)

        selected_entity: str | None = req.COOKIES.get("selected")
        try:
            selected_entity: int = int(selected_entity)
        except TypeError:
            selected_entity: None = None

        print(f"COOKIE GET: {selected_entity} ({type(selected_entity)})")

        #return JsonResponse({"name": "Merge Sort", "type": "partial",    "data": {      "category": ["Sorting", "wrong"],      "year": [1945, "correct"],      "average_time_complexity": ["O(n log n)", "correct"],      "auxiliary_space_complexity": ["O(n)", "partial"],      "data_structure": ["Array", "correct"],      "kind_of_solution": ["Exact", "wrong"],      "generality": ["General-purpose", "wrong"]     }    })
        return GuessView.check_fields(selected_entity, entity)


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