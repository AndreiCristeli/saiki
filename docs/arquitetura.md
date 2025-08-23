# Tecnologias utilizadas e Visão geral da arquitetura do sistema

O sistema adota uma arquitetura cliente-servidor da seguinte forma:

- **Frontend**: desenvolvido em HTML5 e CSS, responsável pela interface gráfica e interação com o usuário.
- **Backend e Banco de Dados**: utilizam o framework web Django na linguagem Python para fornecer os elementos do banco, processar as jogadas do usuário e realizar
a configuração dos cookies da página.

O fluxo do sistema consiste em: coletar as requisições (no caso, jogadas) do usuário, alterar o estado do jogo pelo Backend, que repassa as mudanças realizadas
para o Frontend, que por sua vez, atualiza a tela do usuário conforme a entrada recebida.
