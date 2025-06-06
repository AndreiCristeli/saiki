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

function click(event, button) {
  const dialog = document.querySelector('.infoDialog');
  if (dialog) {
    dialog.showModal();
  }  
}

function closeDialog(event, dialog) {
  if(dialog) {
    dialog.style.animation = 'desvanecer 0.8s ease-out forwards';

    dialog.addEventListener('animationend', function handleClose() {
      dialog.close();
      dialog.style.animation = '';
      dialog.removeEventListener('animationend', handleClose);
    });
  }
}

i18next.init({
  lng: 'pt', // idioma inicial
  debug: true,
  resources
}, function(err, t) {
  updateContent();
});

function updateContent() {
  document.querySelector('h1').textContent = i18next.t('title');
  document.querySelector('p').textContent = i18next.t('question');
  document.querySelector('.Input').placeholder = i18next.t('inputPlaceholder');
  document.querySelector('.attempts').textContent = i18next.t('attempts', { count: tentativas });

  const labels = document.querySelectorAll('.label li');
  const keys = [
    'categoryInfoTitle',
    'yearInfoTitle',
    'timeInfoTitle',
    'spaceInfoTitle',
    'structureInfoTitle',
    'solutionInfoTitle',
    'generalityInfoTitle'
  ];

  labels.forEach((el, idx) => {
    el.textContent = i18next.t(keys[idx]);
  });

  document.querySelector('.howToPlayTitle').textContent = i18next.t('howToPlay');
  document.querySelector('.howToPlayDesc').textContent = i18next.t('description');

  document.querySelector('.categoryTitle').textContent = i18next.t('categoryInfoTitle');
  document.querySelector('.categoryText').textContent = i18next.t('categoryInfoText');

  document.querySelector('.yearTitle').textContent = i18next.t('yearInfoTitle');
  document.querySelector('.yearText').textContent = i18next.t('yearInfoText');

  document.querySelector('.timeTitle').textContent = i18next.t('timeInfoTitle');
  document.querySelector('.timeText').textContent = i18next.t('timeInfoText');

  document.querySelector('.spaceTitle').textContent = i18next.t('spaceInfoTitle');
  document.querySelector('.spaceText').textContent = i18next.t('spaceInfoText');

  document.querySelector('.structureTitle').textContent = i18next.t('structureInfoTitle');
  document.querySelector('.structureText').textContent = i18next.t('structureInfoText');

  document.querySelector('.solutionTitle').textContent = i18next.t('solutionInfoTitle');
  document.querySelector('.solutionText').textContent = i18next.t('solutionInfoText');

  document.querySelector('.generalityTitle').textContent = i18next.t('generalityInfoTitle');
  document.querySelector('.generalityText').textContent = i18next.t('generalityInfoText');
}

function trocarIdioma(lang) {
  i18next.changeLanguage(lang, () => {
    updateContent();
  });
}
