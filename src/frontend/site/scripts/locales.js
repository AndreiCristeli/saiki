/** 
 * @file frontend/site/script/locale.js
 * 
 * @author AndreiCristeli
 * 
 * @version 0.2
 */

const resources = {
  pt: {
    translation: {
      daily: "Diário",
      trueOrFalse: "Verdadeiro ou Falso",
      custom: "Personalizado",
      index_question: "Qual é o algoritmo do dia?",
      custom_question: "Qual é o algoritmo?",
      inputPlaceholder: "Escreva aqui",
      attempts: "Tentativas: ",
      tof_question: "É verdadeiro ou falso?",
      howToPlay: "Como jogar",
      howToPlayTOF: "Responda as perguntas com verdairo ou falso com base nos seus conhecimentos.",
      topicsTextTOF: "Perguntas estas que são separadas por temas da computação.",
      scoreTextTOF: "Pontuação de 0 a 5 de acordo com a quantidade de acertos.",
      topicsTitleTOF: "Tópicos",
      scoreTitleTOF: "Pontuação",
      description: "Você deve adivinhar o algoritmo do dia se baseando nas pistas.",
      categoryInfoTitle: "Categoria",
      categoryInfoText: "O tipo ou propósito geral do algoritmo. Ex: ordenação, busca, grafos, otimização, geometria computacional.",
      yearInfoTitle: "Ano",
      yearInfoText: "Ano de criação ou publicação do algoritmo. Refere-se ao momento em que o algoritmo foi proposto ou documentado pela primeira vez.",
      timeInfoTitle: "Complexidade Temporal Média",
      timeInfoText: "Tempo esperado que o algoritmo leva para executar em casos comuns. Representada em notação Big-O: O(n), O(n log n), etc.",
      spaceInfoTitle: "Complexidade Espacial Auxiliar",
      spaceInfoText: "Memória extra necessária além da entrada original. Também expressa em Big-O, como O(1), O(n). Não conta a memória ocupada pelos dados de entrada.",
      structureInfoTitle: "Estrutura de Dados",
      structureInfoText: "As estruturas usadas para processar a informação. Ex: listas, filas, pilhas, árvores, heaps, tabelas hash.",
      solutionInfoTitle: "Solução",
      solutionInfoText: "Tipo de abordagem adotada pelo algoritmo. Exata: resolve o problema com resposta correta garantida. Aproximada: gera uma solução próxima da ideal. Heurística: usa regras práticas para encontrar boas soluções.",
      generalityInfoTitle: "Generalidade",
      generalityInfoText: "O algoritmo soluciona qualquer tipo de problema dentro da sua categoria ou exige certas condições? Ex: BubbleSort ordena qualquer vetor. RadixSort exige inteiros."
    }
  },
  en: {
    translation: {
      daily: "Daily",
      trueOrFalse: "True or False",
      custom: "Custom",
      index_question: "What is today's algorithm?",
      custom_question: "What is the algorithm?",
      inputPlaceholder: "Type here",
      attempts: "Attempts: ",
      tof_question: "Is True or False?",
      howToPlay: "How to play",
      howToPlayTOF: "Answer the questions true or false based on your knowledge.",
      topicsTextTOF: "These questions are separated by computing topics.",
      scoreTextTOF: "Scores range from 0 to 5 based on the number of correct answers.",
      topicsTitleTOF: "Topics",
      scoreTitleTOF: "Score",
      description: "You must guess the algorithm of the day based on the clues.",
      categoryInfoTitle: "Category",
      categoryInfoText: "The general type or purpose of the algorithm. E.g., sorting, search, graphs, optimization, computational geometry.",
      yearInfoTitle: "Year",
      yearInfoText: "Year of creation or publication. Refers to when the algorithm was first proposed or documented.",
      timeInfoTitle: "Average Time Complexity",
      timeInfoText: "Expected time the algorithm takes to run on typical input. Expressed in Big-O notation: O(n), O(n log n), etc.",
      spaceInfoTitle: "Auxiliary Space Complexity",
      spaceInfoText: "Extra memory needed beyond the input. Also in Big-O, like O(1), O(n). Does not count the memory used by input.",
      structureInfoTitle: "Data Structure",
      structureInfoText: "Structures used to process data. E.g., lists, queues, stacks, trees, heaps, hash tables.",
      solutionInfoTitle: "Solution",
      solutionInfoText: "Approach type. Exact: gives guaranteed correct answer. Approximate: gives near-optimal solution. Heuristic: uses practical rules for good (but not guaranteed) answers.",
      generalityInfoTitle: "Generality",
      generalityInfoText: "Does it solve any problem in its category or does it need specific conditions? E.g., BubbleSort works on any list; RadixSort needs integers."
    }
  },
  es: {
    translation: {
      daily: "Diario",
      trueOrFalse: "Verdadero o Falso",
      custom: "Personalizado",
      index_question: "¿Cuál es el algoritmo del día?",
      custom_question: "¿Cuál es el algoritmo?",
      inputPlaceholder: "Escribe aquí",
      attempts: "Intentos: ",
      tof_question: "¿Es verdadero o falso?",
      howToPlay: "Cómo jugar",
      howToPlayTOF: "Responde las preguntas con verdadero o falso según tus conocimientos.",
      topicsTextTOF: "Estas preguntas están organizadas por temas de computación.",
      scoreTextTOF: "Puntuación de 0 a 5 según la cantidad de aciertos.",
      topicsTitleTOF: "Temas",
      scoreTitleTOF: "Puntuación",
      description: "Debes adivinar el algoritmo del día basándote en las pistas.",
      categoryInfoTitle: "Categoría",
      categoryInfoText: "El tipo o propósito general del algoritmo. Ej.: ordenación, búsqueda, grafos, optimización, geometría computacional.",
      yearInfoTitle: "Año",
      yearInfoText: "Año de creación o publicación del algoritmo. Se refiere al momento en que fue propuesto o documentado por primera vez.",
      timeInfoTitle: "Complejidad Temporal Promedio",
      timeInfoText: "Tiempo esperado que el algoritmo tarda en ejecutarse en casos comunes. Representado en notación Big-O: O(n), O(n log n), etc.",
      spaceInfoTitle: "Complejidad Espacial Auxiliar",
      spaceInfoText: "Memoria extra necesaria además de la entrada original. También expresada en Big-O, como O(1), O(n). No cuenta la memoria ocupada por los datos de entrada.",
      structureInfoTitle: "Estructura de Datos",
      structureInfoText: "Las estructuras utilizadas para procesar la información. Ej.: listas, colas, pilas, árboles, montículos, tablas hash.",
      solutionInfoTitle: "Solución",
      solutionInfoText: "Tipo de enfoque adoptado por el algoritmo. Exacta: resuelve el problema con respuesta garantizada. Aproximada: genera una solución cercana a la ideal. Heurística: usa reglas prácticas para encontrar buenas soluciones.",
      generalityInfoTitle: "Generalidad",
      generalityInfoText: "¿El algoritmo resuelve cualquier tipo de problema dentro de su categoría o requiere condiciones específicas? Ej.: BubbleSort ordena cualquier vector. RadixSort requiere enteros."
    }
  }
};
