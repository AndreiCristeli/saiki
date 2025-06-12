# Requisitos
## Histórias de Usuário

### Jogador
- **H01**:
  - Eu como Jogador gostaria de Jogar o modo de adivinhação de temas da computação.

- **H02:** 
  - Eu como Jogador gostaria de jogar o modo de Verdadeiro ou Falso.

- **H03**:
  - Eu como Jogador gostaria de compartilhar minhas estatísicas de jogo com meus amigos.

- **H04**:
  - Eu como Jogador gostaria de visualizar sugestões de resposta baseadas no que escrevi.

- **H05**:
  - Eu como Jogador gostaria de fazer meu cadastro de usuário no sistema.
 
- **H06**:
  - Eu como Jogador gostaria de visualizar minhas estatísticas de jogo.
 
- **H07**:
  - Eu como Jogador gostaria de visualizar o meu histórico de jogo.
 
- **H08**:
  - Eu como Jogador Gostaria de Vizualizar um manual de usuário.
 
- **H09**:
  - Eu como Jogador gostaria de: Jogar o modo Multi-jogador.

 ### Adminstrador
- **H10**:
  - Eu como Administrador gostaria de gerenciar o conteúdo de cada modo de jogo.

- **H11**:
  - Eu como Administrador gostaria de visualizar os conteúdos de cada modo de jogo.

- **H12**:
  - Eu como Administrador gostaria de visualizar estatísticas gerais de todos os usuários.

- **H13**:
  - Eu como Administrador gostaria de gerenciar logins.



## Casos de Uso

### **UC01**: Jogador gostaria de Jogar o modo de adivinhação de temas da computação.

- **Ator:** Jogador
- **Fluxo Normal:**
  1. Visitante entra no site.
  1. Jogador acessa o modo de jogo de Adivinhação.
  1. Jogo seleciona o tópico para adivinhação.
  1. Jogador informa a tentativa.
  1. Jogo informa se o jogador venceu. Se não venceu, volta pra (4).
  1. Exibir opção de compartilhamento.

- **Extenções:** 
  - **5a:** Se Jogador sair da partida, salvar seu progresso para que seja possível retornar no mesmo estado.

### **UC02**: Jogador gostaria de jogar o modo de Verdadeiro ou Falso.

- **Ator:** Jogador
- **Fluxo Normal:**
  1. Visitante entra no site.
  1. Jogador acessa o modo de jogo de Verdadeiro ou Falso.
  1. Jogo seleciona uma pergunta.
  1. Jogador informa a tentativa.
  1. Jogo informa se o jogador venceu. Se não venceu, volta pra (4).
  1. Exibir opção de compartilhamento.