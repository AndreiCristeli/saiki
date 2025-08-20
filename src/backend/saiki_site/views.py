"""
backend/saiki_site/views.py

Viewing configuration for saiki_site Django's application.
"""

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .guesser import guesser, GuessState
# from typing import Any
import json
import uuid
from typing import Any, Dict, List
# from django.http import WSGIRequest
import random
from django.utils import timezone

from os import path



class FrontendView(object):
    """Handles the view of the frontend via the backend."""

    @staticmethod
    def serve_frontend(req) -> HttpResponse:
        """Provides the frontend main page."""
        

        # inferring the request...
        print(type(req), req)

        # the html source
        index_path: str = path.join(path.dirname(__file__), "../../frontend/site/html/index.html")

        # opening and sending the HTML over
        with open(index_path, encoding="utf-8") as index:
            return HttpResponse(index.read(), content_type="text/html")

    @staticmethod
    def serve_custom_mode(request):
        return render(request, "custom.html")

    @staticmethod
    def serve_daily_mode(request):
        return render(request, "index.html")

    @staticmethod
    def serve_tof_mode(request):
        return render(request, "trueOrFalse.html")


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
        return GuessState.from_request(req).guess_diary(entity)

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
    

class TrueOrFalseGameLogic:
    """Contains the game logic for True or False mode."""

    @classmethod
    def validate_question(cls, current_question, questions):
        for q in questions:
            if current_question['id'] == q['id']:
                return False

        return True

    @classmethod
    def generate_questions(cls, count: int = 10) -> List[Dict[str, Any]]:
        """Generate random true/false questions about algorithms."""
        questions = []
        
        # questions_path = "../../../data/tf_template.json"
        questions_path: str = path.join(path.dirname(__file__), "../../../data/tf_template.json")
        
        with open(questions_path, 'r', encoding='utf-8') as file:
            all_questions = json.load(file)
                    
        collected = 0
        
        while collected < count:           
            choice = random.choice(all_questions)
            
            question = {
                'area': choice['area'],
                'question': choice['pergunta'],
                'correct_answer': choice['resposta'],
                'id' : choice['id']
            }
            if not cls.validate_question(question,questions):
                continue
            
            questions.append(question)
            collected += 1 
        
        return questions


    @classmethod
    def validate_answer(cls, question: Dict[str, Any], user_answer: bool) -> bool:
        """Validate if the user's answer is correct."""
        return user_answer == question['correct_answer']

"""
Correções para o sistema True or False
"""

class TrueOrFalseState:
    """Manages the state of a True or False game session."""
    
    def __init__(self, session_data: Dict[str, Any]):
        self.session_data = session_data
        self.session_id = session_data.get('session_id')
    
    @classmethod
    def from_request(cls, request: WSGIRequest, session_id: str) -> 'TrueOrFalseState':
        """Load game session from cookies."""
        cookie_key = f'tof_session_{session_id}'
        
        if cookie_key not in request.COOKIES:
            raise ValueError("Sessão não encontrada")
        
        try:
            # print(f"Recuperando cookie: {cookie_key}")
            session_data = json.loads(request.COOKIES[cookie_key])
            return cls(session_data)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON do cookie: {e}")
            raise ValueError("Dados da sessão corrompidos")
    
    def update_cookie(self, response: HttpResponse) -> HttpResponse:
        """Atualiza o cookie com o estado atual da sessão."""
        cookie_key = f'tof_session_{self.session_id}'
        response.set_cookie(
            key=cookie_key,
            value=json.dumps(self.session_data),
            max_age=3600,  # 1 hora
            httponly=True,
            samesite='Lax'
        )
        return response
    
    def process_answer(self, question_index: int, user_answer: bool) -> Dict[str, Any]:
        """Process a user's answer to a question."""

        # Debug
        print(f"Processing answer for question {question_index}")
        
        # Verificar se a questão existe
        if question_index >= len(self.session_data['questions']):
            raise ValueError("Índice de questão inválido")
        
        question = self.session_data['questions'][question_index]
        
        # Converter question_index para string para usar como chave
        question_key = str(question_index)
        
        # Verificar se já foi respondida
        if question_key in self.session_data['answers']:
            return {
                'is_correct': self.session_data['answers'][question_key] == question['correct_answer'],
                'correct_answer': question['correct_answer'],
                'already_answered': True,
                'score': self.session_data['score'],
                'answered_questions': self.session_data['answered_questions'],
                'total_questions': self.session_data['total_questions']
            }
        
        # Validar resposta
        is_correct = user_answer == question['correct_answer']
        
        # Atualizar estado
        self.session_data['answers'][question_key] = user_answer
        self.session_data['answered_questions'] += 1
        
        if is_correct:
            self.session_data['score'] += 1
        
        # print(f"Score atualizado: {self.session_data['score']}")
        # print(f"Respostas até agora: {self.session_data['answers']}")
        
        return {
            'is_correct': is_correct,
            'correct_answer': question['correct_answer'],
            'already_answered': False,
            'score': self.session_data['score'],
            'answered_questions': self.session_data['answered_questions'],
            'total_questions': self.session_data['total_questions']
        }


class TrueOrFalseView(object):
    """Handles the view of the True or False game mode."""

    @staticmethod
    def empty() -> JsonResponse:
        """Represents an empty JSON response."""
        return JsonResponse({})

    @staticmethod
    @csrf_exempt
    def start_game(req: WSGIRequest) -> JsonResponse:
        """Starts a new True or False game session, via POST."""
        
        if req.method != "POST":
            return TrueOrFalseView.empty()

        try:
            session_id = str(uuid.uuid4())
            questions = TrueOrFalseGameLogic.generate_questions(5)
            
            # print(f"Iniciando nova sessão: {session_id}")
            # print(f"Número de questões geradas: {len(questions)}")
            
            game_session = {
                'session_id': session_id,
                'questions': questions,
                'answers': {},  # Dicionário vazio para armazenar respostas
                'score': 0,
                'answered_questions': 0,
                'total_questions': len(questions),
                'created_at': timezone.now().isoformat()
            }
            
            # Criar resposta com dados do jogo
            response_data = {
                'session_id': session_id,
                'questions': questions,
                'total_questions': len(questions),
                'message': 'Jogo iniciado com sucesso'
            }
            
            response = JsonResponse(response_data)
            
            # Definir cookie com a sessão completa
            response.set_cookie(
                key=f'tof_session_{session_id}',
                value=json.dumps(game_session),
                max_age=3600,  # 1 hora
                httponly=True,
                samesite='Lax'
            )
            
            return response
            
        except Exception as e:
            print(f"Erro ao iniciar jogo True or False: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': 'Erro interno do servidor'}, status=500)

    @staticmethod
    @csrf_exempt
    def submit_answer(req: WSGIRequest) -> JsonResponse:
        """Processes the submission of an answer, via POST."""
        
        if req.method != "POST":
            return TrueOrFalseView.empty()

        try:
            data: dict = json.loads(req.body)
            
            # Extrair dados da requisição
            session_id: str = data.get("session_id")
            question_index: int = data.get("question_index")
            user_answer: bool = data.get("answer")
            
            # print(f"Recebido: session_id={session_id}, question_index={question_index}, answer={user_answer}")
            
            # Validação de tipos
            if session_id is None or not isinstance(session_id, str):
                raise ValueError("session_id inválido ou ausente")
            if question_index is None or not isinstance(question_index, int):
                raise ValueError("question_index inválido ou ausente")
            if user_answer is None or not isinstance(user_answer, bool):
                raise ValueError("answer deve ser um booleano")

        except (TypeError, KeyError, ValueError, json.JSONDecodeError) as e:
            print(f"Erro ao processar dados: {e}")
            return JsonResponse({'error': f'Dados inválidos: {str(e)}'}, status=400)

        try:
            # Recuperar estado do jogo
            tof_state = TrueOrFalseState.from_request(req, session_id)
            
            # Processar resposta
            result = tof_state.process_answer(question_index, user_answer)
            
            # IMPORTANTE: Criar resposta e atualizar cookie
            response = JsonResponse(result)
            response = tof_state.update_cookie(response)
            
            return response
            
        except ValueError as e:
            print(f"Erro de validação: {e}")
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            print(f"Erro inesperado ao processar resposta: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': 'Erro ao processar resposta'}, status=500)

    @staticmethod
    @csrf_exempt
    def get_results(req: WSGIRequest) -> JsonResponse:
        """Retorna os resultados finais do jogo."""
        
        if req.method != "POST":
            return TrueOrFalseView.empty()
        
        try:
            data: dict = json.loads(req.body)
            session_id: str = data.get("session_id")
            
            if not session_id:
                raise ValueError("session_id não fornecido")
            
            # Recuperar estado do jogo
            tof_state = TrueOrFalseState.from_request(req, session_id)
            
            # Preparar resultados detalhados
            results = {
                'final_score': tof_state.session_data['score'],
                'total_questions': tof_state.session_data['total_questions'],
                'answered_questions': tof_state.session_data['answered_questions'],
                'percentage': round((tof_state.session_data['score'] / tof_state.session_data['total_questions']) * 100, 2),
                'answers': tof_state.session_data['answers'],
                'questions': tof_state.session_data['questions']
            }
            
            return JsonResponse(results)
            
        except Exception as e:
            print(f"Erro ao obter resultados: {e}")
            return JsonResponse({'error': 'Erro ao obter resultados'}, status=500)



#-------------------------------------------------------------------------------------------
from .forms import JogadorForm, JogadorLoginForm, MessageForm
from .models import Jogador, Session, message
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



def criar_sessao(request):
    if not request.user.is_authenticated:
        return redirect('login')  # ou outra view

    jogador = Jogador.objects.get(user=request.user)

    # Gera chave única com name_user + timestamp
    timestamp = int(time.time())
    public_key = f"{jogador.name_user}_{timestamp}"

    # Cria a sessão (chat será criado automaticamente no save())
    sessao = Session.objects.create(
        public_key=public_key,
        root_player=jogador,
    )

    return redirect('ver_sessao', sessao_id=sessao.id)

from django.shortcuts import render, get_object_or_404, redirect

def ver_sessao(request, sessao_id):
    if not request.user.is_authenticated:
        return redirect('login')

    jogador = Jogador.objects.get(user=request.user)
    sessao = get_object_or_404(Session, id=sessao_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid() and sessao.status:
            texto = form.cleaned_data['texto']

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

            return redirect('ver_sessao', sessao_id=sessao.id)

    else:
        form = MessageForm()

    tempo_corrente = timezone.now() - sessao.data_inicio if sessao.status else sessao.session_time
    mensagens = sessao.chat.messages.order_by('timestamp')

    return render(request, 'sessao.html', {
        'sessao': sessao,
        'jogador': jogador,
        'mensagens': mensagens,
        'tempo_corrente': tempo_corrente,
        'form': form,
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

    return redirect('painel_jogador')


