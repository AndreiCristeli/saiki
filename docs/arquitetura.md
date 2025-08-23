# Arquitetura geral do Sistema

## Tecnologias Utilizadas

- **Frontend**: HTML5, JavaScript
- **Midend**: Python (Django)
- **Backend**: Python (Django)
- **Tests**: Selenium

## Organização

O projeto foi estruturado da seguinte forma: Dividiu-se a implementação entre frontend e backend de modo que no backend, foi definida toda a configuração do ambiente `django`, com alguns scripts adcionais para a lógica do jogo, enquanto que, no frontend, uma abordagem mais livre foi adotada com a consturção de um ambiente web construído com o básico das ferramentas HTML, CSS e JavaScript.

### Backend

No backend, a codificação seguiu bastante as definições do framework do `django`, sendo que a principal decisão estrutural foi a divisão do projeto em duas aplicações separadas: uma específica para o gerenciamento e manipulação do banco de dados (`saiki_data`) e uma para a lógica interna do jogo (`saiki_site`), incluindo a comunicação com a lógica do fontend.

Os principais módulos implentados no backend são:

- **GuessView**: define os servidores das diferentes páginas visíveis aos usuários no modo de adivinhação.

- **TrueOrFalseView**: define os servidores das diferentes páginas visíveis aos usuários no modo verdaeiro ou falso.

- **TrueOrFalseGameLogic**: define a lógica intrerna do modo verdadeiro ou falso.

- **PlayerView**: define os serviços de login, autenticação e registro do usuário no site.

- **SaikiEntityDatabase**: define a lógica necessária para o gerenciamento e manipulação da base de dados referente às entidades (Algoritmos, personalidades, etc.) jogáveis. Manipula o banco de dados `saiki_data_db.sqlite3`.

- **Jogador**: define a lógica necessária para o gerenciamento da base de dados de Jogadores. Manipula o banco de dados `db.sqlite3`.

- **Session**: define a lógica necessária para o gerenciamento da base de dados de Sessões. Manipula o banco de dados `db.sqlite3`.

- **GuessState**: Gerencia e manipula o estado de jogoa atual de um nogador no modo de adivinhação. Comunica-se o módulo `Hints` do frontend.

### Frontend

Para o frontend foram implementadas páginas web utilizando HTML5 e CSS3 puros com scripts em JavaScript. Nesse sentido, uma flexibilidade maior foi adotada nessa parte do projeto.

Os principais módulos implentados no frontend são:

- **API**: define a api utilizada para comunicação com o backend utilizando o protocolo HTTP e mensagens em formato json.

- **AttemptsHandler**: Define a lógica relativa ao tratamento das tentativas entradas pelo usuário no modo de adivinhação.

- **Hints**: define a lógica necessária para a mostragem de dicas baseadas no input do usário. Comunica-se o módulo `GuessState` do backend.

- **InputHandler**: Gerencia o tratamento das entradas do usuário de uma forma geral. Esse módulo é compartilhado entre os deiferentes modos de jogo.

- **Renderer**: Representa um renderizador para os elementos dinâmicos das páginas do site. Esse módulo é compartilhado entre os deiferentes modos de jogo.

- **Translate**: Define as opções de traduções e localizações de textos do site.

A relação dependencia estrutural entre esses componetes está apresentada a seguir:
```
main_script
├── Renderer
│   └── InputHandler
│       ├── Hints -> API
│       └── AttemptsHandler -> API
└── Translate
```


## Estrutura do projeto

A seguir apresenta-se a estrutra do projeto no formato de árvore de arquivos:
```
saiki/
├── src/
│   ├── backend/
│   │   ├── core/
│   │   │   └── enc.py
│   │   │
│   │   ├── saiki_data/ (A aplicação django referente ao banco de dados)
│   │   │   ├── migrations/
│   │   │   │   └── [django migrations] ...
│   │   │   ├── templates/
│   │   │   │   └── [database json templates] ...
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── database.py
│   │   │   ├── entities.py
│   │   │   ├── load_json.py
│   │   │   ├── models.py
│   │   │   └── urls.py
│   │   │
│   │   ├── saiki_django/ (As definições do projeto django)
│   │   │   ├── asgi.py
│   │   │   ├── router.py
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   └── wsgi.py
│   │   │   
│   │   ├── saiki_site/ (A aplicação django ao site em si)
│   │   │   ├── migrations/
│   │   │   │   └── [django migrations] ...
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── forms.py
│   │   │   ├── guesser.py
│   │   │   ├── models.py
│   │   │   ├── msgs.py
│   │   │   ├── player_views.py
│   │   │   ├── tests.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   │
│   │   ├── main.py
│   │   ├── manage.py
│   │   ├── db.sqlite3
│   │   ├── saki_data_db.sqlite3
│   │   └── Makefile
│   │
│   └── frontend/
│       ├── assets/
│       │   └── [saiki assests] ...
│       │
│       ├── dependecies/
│       │   └── katex/
│       │       └── [katex files]...
│       │
│       └── site/
│           ├── css/
│           │   └── [css files]...
│           │
│           ├── html/
│           │   ├── templates/
│           │   │   ├── player_form.html
│           │   │   ├── player_login.html
│           │   │   ├── player_panel.html
│           │   │   └── session.html
│           │   ├── custom.html
│           │   ├── index.html
│           │   └── trueOrFalse.html
│           │
│           └── scripts/
│               ├── api.js
│               ├── attempt.js
│               ├── easter_eggs.js
│               ├── hints.js
│               ├── input_handler.js
│               ├── locale.js
│               ├── main_guess.js
│               ├── main_true_or_false.js
│               ├── renderer.js
│               └── translate.js
|   
└── tests/      
    └-─ Saiki_Tests.side

```