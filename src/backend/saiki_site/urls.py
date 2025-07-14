"""
backend/saiki_site/urls.py

URL configuration for saiki_site Django's application.
"""

from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver
from . import views


urlpatterns: list[URLPattern | URLResolver] = [
    path("", views.FrontendView.serve_frontend),

    # Testing
    path("api/cmrd/", views.OtherView.read_root),
    path("api/hangar/", views.read_root1),

    # Guess mode requests
    path("api/guess/hint/", views.GuessView.request_hint),
    path("api/guess/entity/", views.GuessView.request_entity),


    # Models URLS
    path('jogador/novo/', views.jogador_create, name='jogador_create'),
    path('jogador/sucesso/', views.jogador_success, name='jogador_success'), 
    path('login/', views.jogador_login, name='jogador_login'),
    path('register/', views.jogador_create, name='jogador_register'),
    path('painel/', views.painel_jogador, name='painel_jogador'),
    path('criar-sessao/', views.criar_sessao, name='criar_sessao'),
    path('sessao/<int:sessao_id>/', views.ver_sessao, name='ver_sessao'),
    path('sessao/<int:sessao_id>/encerrar/', views.encerrar_sessao, name='encerrar_sessao'),
    path('entrar-sessao/', views.entrar_sessao, name='entrar_sessao'),




]
