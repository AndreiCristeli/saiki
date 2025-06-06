var tentativas = 0
window.onload = function () {
  const input = document.querySelector('.Input');
  const element = document.querySelector('.attempts')
  input.addEventListener('keydown', (event) => keydown(event, input, element));

  const button = document.querySelector('.footer-info');
  button.addEventListener('click', (event) => click(event, button));

  const closeBtn = document.querySelector('.closeDialog');
  if (closeBtn) {
    const dialog = document.querySelector('.infoDialog');
    closeBtn.addEventListener('click', (event) => closeDialog(event, dialog));
  }
};

function keydown(event, input, element) {
  if (event.key === 'Enter') {
    const valorDigitado = event.target.value.trim();
    console.log('Valor digitado:', valorDigitado);
    input.value = '';

    if(valorDigitado) {
      
      tentativas++;
      element.textContent = `Tentativas: ${tentativas}`;  
      var varia;
      if(false) {
        varia = 'card correct';
      }
      else {
        varia = 'card wrong';
      }

      /*Faz busca banco de Dados*/
      
      // Função para criar e adicionar um novo card
      function adicionarCard() {
        // Cria o elemento da div com class="card"
        const card = document.createElement('div');
        card.className = varia;

        // Adiciona o cabeçalho do card
        const header = document.createElement('div');
        header.className = 'card-header';
        header.textContent = valorDigitado; // nome do algoritmo
        card.appendChild(header);

        // Cria a grade de informações
        const infoGrid = document.createElement('div');
        infoGrid.className = 'info-grid';

        // Lista com os dados (você deve ajustar usando o banco de dados)
        const dados = [
          'Ordenação',           // Categoria
          '1960',                // Ano
          'T ∈ O(n log n)',      // Complexidade temporal
          'S ∈ O(log n)',        // Complexidade espacial
          '[]',                  // Estrutura de dados
          'Exata',               // Solução
          'Geral'                // Generalidade
        ];

        // Para cada item, cria uma div com classe "info-item correct-color"
        dados.forEach(texto => {
          const infoItem = document.createElement('div');
          infoItem.className = 'info-item wrong-color';
          infoItem.textContent = texto;
          infoGrid.appendChild(infoItem);
        });

        // Adiciona o info-grid ao card
        card.appendChild(infoGrid);
        
        // Insere o card no body ou em outro container (ex: abaixo do último card)
        const container = document.querySelector('.cards-container');
        container.insertBefore(card, container.firstChild);
      }

        // Exemplo: chama a função para adicionar um novo card ao carregar a página
      adicionarCard();
    }
  }

}
