/** 
 * @file frontend/site/script/input_handler.js
 * 
 * @author AndreiCristeli
 * @author victorxaviercosta
 * 
 * @version 0.1
 */

import { AttemptsHandler, ATTEMPT_RC } from "./attempt.js"
import { Hints } from "./hints.js"

import * as eg from "./easter_eggs.js"
import { api } from "./api.js";

// TODO: Handle entity_type properly according to user's selection.
const ENTITY_TYPE_PH = "Algorithm"

export class InputHandler {
	constructor(renderer){
		this.hints = new Hints(renderer)
		this.attempt_handler = new AttemptsHandler(renderer)

		
		this.current_game_session = null;
		this.current_question_index = 0;
		this.renderer = renderer;
	}
	
	// Normalizes user's input.
	// Returns all input words captalized (Change as needed for the backend database).
	#__normalize_input(input) {
		let trimmed = input.trim(); // Removes leading and trailing spaces (but not spaces between words).
		return trimmed.toLowerCase();
	}


	// Event handler for input event on the input text box. (Essetialy handles text changes).
	input_on_text_change(event){
		this.user_input = this.#__normalize_input(event.target.value); 
		// console.log(`Nomalized Input: ${this.user_input}`);
	
		// In the case there's no input in the text-box
		if (!this.user_input){
			this.hints.hide();
			return;
		}
	
		//console.log(event.target.value);
		this.hints.display(this.user_input);
	}

	// Event handler for keydown on the input text box. (Essentialy handles navigation).
	async input_on_keydown(event) {
		if ((event.key == "ArrowUp") && this.hints.is_displaying()) {
			// console.log("arrowUp");
			this.hints.move_hint_selection("up");
			
		}else if ((event.key == "ArrowDown") && this.hints.is_displaying()) {
			// console.log("arrowDown");
			this.hints.move_hint_selection("down");
		
		} else if (event.key === 'Enter') {
			console.log("ENTER");
			if (this.hints.is_displaying() === true){
				this.user_input = this.#__normalize_input(this.hints.the_hints[this.hints.selected_hint]);
			}

			await this.process_input();
		}
	}

	async process_input(){
		let input_box = document.querySelector(".Input");
		const current_page = document.body.dataset.page;
		
		this.hints.hide(); // Hinding the Hints
	
		if (this.user_input === "milvus"){
			eg.showMilvusDialog(); input_box.value = ''; return;

		} else if (this.user_input === "pokemon" || this.user_input === "monkepo"){
			eg.showPokemonDialog(); input_box.value = ''; return;
		}

		let attempt_rc = await this.attempt_handler.process_attempt(this.user_input, ENTITY_TYPE_PH);

		switch (attempt_rc) {
			case ATTEMPT_RC.REPEATED_ANSWER: 
			case ATTEMPT_RC.NOT_FOUND:
				break;
			case ATTEMPT_RC.VICTORY: // Win Condition.
				win_condition(input_box, this, current_page);

			default:
				input_box.value = '';
		}
	}

	// Event handler for when clicking on new game.
	// Função para novo jogo (serve para ambos os modos)
	async new_game_click(event, btn) {
		const container = btn.closest(".div_new_game");
		const currentPage = document.body.dataset.page;
		
		// Usar a função reset_game adaptada
		reset_game(container, this);
		
		// Se for True or False, iniciar novo jogo automaticamente
		if (currentPage === "true_or_false") {
			try {
				await this.start_new_tof_game();
			} catch (error) {
				console.error('Erro ao iniciar novo jogo:', error);
			}
		}
	}

	async start_new_tof_game() {
		try {
			console.log('Fazendo chamada para API...');
			const response = await api("/true-or-false/start/", 'POST');
			
			// DEBUG COMPLETO
			console.log('=== RESPOSTA DA API ===');
			console.log('Tipo da resposta:', typeof response);
			console.log('Resposta completa:', response);
			
			// Tentar encontrar questions em diferentes locais
			let gameData = null;
			let questionsFound = false;
			
			if (response.questions) {
				console.log('questions encontrado em response.questions');
				gameData = response;
				questionsFound = true;
			}
			
			this.current_game_session = gameData;

			this.current_question_index = 0;

			// Renderizar as questões
			this.renderer.render_tof_questions(this.current_game_session.questions);

			this.update_tof_game_ui();
			
			console.log('Jogo iniciado com sucesso!');

		} catch (error) {
			console.error('Erro ao iniciar jogo True or False:', error);
			throw error;
		}
	}


	update_tof_game_ui() {
        const session = this.current_game_session;

        // Elementos do placar e progresso
        const scoreField = document.querySelector('.score-field');
        const currentField = document.querySelector('.current-question');
        const totalField = document.querySelector('.total-questions');

        // Elementos do card da questão
        const questionCard = document.querySelector('.tof-question-card'); // Card principal da questão
        const algorithmNameEl = document.querySelector('.tof-question-algorithm');
        const factsContainerEl = document.querySelector('.tof-question-facts');
        
        // Se a sessão do jogo não existir (ex: jogo resetado), limpa a UI.
        if (!session) {
            if (scoreField) scoreField.textContent = '0';
            if (currentField) currentField.textContent = '0';
            if (totalField) totalField.textContent = '10'; // Ou o total padrão
            if (algorithmNameEl) algorithmNameEl.textContent = 'Aguardando novo jogo...';
            if (factsContainerEl) factsContainerEl.innerHTML = '';
            if (questionCard) questionCard.style.display = 'none';
            return;
        }

        // Atualiza o placar e o progresso
        if (scoreField) scoreField.textContent = session.score;
        if (currentField) currentField.textContent = session.answered_questions;
        if (totalField) totalField.textContent = session.total_questions;

        // Pega a questão atual
        const currentQuestion = session.questions[this.current_question_index];

        // Se o jogo acabou (não há mais questões para mostrar)
        if (!currentQuestion) {
            if (algorithmNameEl) algorithmNameEl.textContent = 'Fim de Jogo!';
            if (factsContainerEl) factsContainerEl.innerHTML = '<p>Parabéns pela sua pontuação!</p>';
            // Desabilitar botões de escolha
            document.querySelectorAll('.button_choice').forEach(btn => btn.disabled = true);
            return;
        }

        // Mostra o card da questão
        if (questionCard) questionCard.style.display = 'block';

        // Atualiza o conteúdo do card com os dados da questão atual
        if (algorithmNameEl) {
            algorithmNameEl.textContent = `Sobre o algoritmo: ${currentQuestion.algorithm_name}`;
        }
        
        if (factsContainerEl) {
            // Limpa os fatos da questão anterior
            factsContainerEl.innerHTML = '';
            
            // Cria a lista de fatos da questão atual (excluindo chaves que não são 'fatos')
            const factKeys = Object.keys(currentQuestion).filter(key => 
                !['algorithm_name', 'correct_answer'].includes(key)
            );

            const ul = document.createElement('ul');
            factKeys.forEach(key => {
                const li = document.createElement('li');
                // Formata a chave para ficar mais legível (ex: 'time_complexity' -> 'Time Complexity')
                const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                li.innerHTML = `<strong>${formattedKey}:</strong> ${currentQuestion[key]}`;
                ul.appendChild(li);
            });
            factsContainerEl.appendChild(ul);
        }
	}


	// Event handler for click on the info button.
	info_click() {
		const dialog = document.querySelector('.infoDialog');
		if (dialog) {
			dialog.showModal();
		}  
	}

	// Event handler for click on the close button of the info dialog.
	close_info_dialog(dialog) {
		if(dialog) {
			dialog.style.animation = 'desvanecer 0.8s ease-out forwards';

			dialog.addEventListener('animationend', function handleClose() {
				dialog.close();
				dialog.style.animation = '';
				dialog.removeEventListener('animationend', handleClose);
			});
		}
	}  

	async hint_click(event, hint_element) {
		console.log("CLICK!!!");
		this.user_input = this.#__normalize_input(hint_element.innerText);
		await this.process_input();
	}

	async logout_click(event){
		console.log("saa~sdsdsd");
		await api("/logout/", "GET", null);
	}

	// Nova função para processar resposta global
	async process_global_tof_answer(answer, question_index) {
		console.log(question_index);
		try {
			// Se não há sessão ativa, iniciar uma nova
			if (!this.current_game_session) {
				await reset_game();
			}
			
			// Submeter resposta para a questão atual
			if (question_index < this.current_game_session.questions.length) {
				console.log("Enviando resposta...");
				console.log(question_index);
				await this.submit_answer(question_index, answer);
				this.current_question_index++;
				
				// Verificar se o jogo terminou
				if (this.current_question_index >= this.current_game_session.questions.length) {
					this.handle_game_end();
				}
			}
		} catch (error) {
			console.error('Erro ao processar resposta:', error);
		}
	}

	// Adicione estes logs na função submit_answer para diagnosticar:
	async submit_answer(question_index, answer) {
		try {
			let entity = {
				session_id: this.current_game_session.session_id,
				question_index: question_index,
				answer: answer
			}
			
			const response = await api('/true-or-false/answer/', 'POST', entity);

			// Use apenas os dados do servidor:
			if (response) {
				this.current_game_session.score = response.score;
				this.current_game_session.answered_questions = response.answered_questions;
				this.current_game_session.total_questions = response.total_questions;
			}

			// Atualizar UI da questão
			this.renderer.update_tof_question_ui(
				question_index, 
				response.is_correct, 
				answer, 
				response.correct_answer
			);
			console.log()
						
			this.update_game_ui();

		} catch (error) {
			console.error('Erro ao submeter resposta:', error);
			throw error;
		}
	}

	// Atualizar UI do jogo
	update_game_ui() {
		const scoreField = document.querySelector('.score-field');
		const currentField = document.querySelector('.current-question');
		const totalField = document.querySelector('.total-questions');
		
		if (scoreField) scoreField.textContent = this.current_game_session.score;
		if (currentField) currentField.textContent = this.current_game_session.answered_questions;
		if (totalField) totalField.textContent = this.current_game_session.total_questions;
	}

	// Lidar com fim de jogo
	handle_game_end() {
		const score = this.current_game_session.score;
		const total = this.current_game_session.total_questions;
		
		setTimeout(() => {
			alert(`Jogo finalizado! Pontuação: ${score}/${total}`);
			
			// Mostrar botão de novo jogo
			const newGameDiv = this.show_new_game_option();

			//  Se a div foi criada, rolar até ela
			if (newGameDiv) {
				document.body.scrollIntoView({ behavior: "smooth" });
			}
		}, 500);
	}

	// Mostrar opção de novo jogo
	show_new_game_option() {
    const container = document.querySelector('.cards-container');
    if (container) {
			const newGameDiv = document.createElement('div');
			newGameDiv.className = 'div_new_game';
			newGameDiv.innerHTML = `
				<p>Parabéns! Jogo finalizado! 🎉</p>
				<button class="btn_new_game">Novo Jogo</button>
			`;
			
			const newGameBtn = newGameDiv.querySelector('.btn_new_game');
			newGameBtn.addEventListener('click', () => reset_game(container, this));
			
			container.parentNode.append(newGameDiv, container);

			return newGameDiv;
    }
    return null;
	}
}

// TODO: rethink where these methods (win_condition and reset_game should go)

/** Handles the Player's win condition. */
function win_condition(input, input_handler, current_page) {
    input.disabled = true;

    // Adding New Game Div Element.
    const div = document.createElement("div");
    div.textContent = "Parabéns! Você venceu! 🎉";
    div.className = "div_new_game";

		// Only permisse in custom game
		if(current_page === "custom") {
			// Adding New Game Button.
			const btn = document.createElement("button");
			btn.textContent = "Novo Jogo";
			btn.className = "btn_new_game";
			btn.addEventListener("click", (event) => input_handler.new_game_click(event, btn));
				
			// Appending New Game's Button as a Child of New Game Div.
			div.appendChild(btn);
		}
		
		input.parentNode.replaceChild(div, input);
}

/** Resets the Player's Game State in the frontend context. */
function reset_game(container, input_handler) {
    const currentPage = document.body.dataset.page;
    
    // Limpeza comum para ambos os modos
    const cardsContainer = document.querySelector(".cards-container");
    const newGameContainer = document.querySelector(".div_new_game");
    if (cardsContainer) {
        cardsContainer.innerHTML = "";
    }
     
	if (currentPage === "true_or_false") {
        // Lógica específica do modo True or False
        reset_tof_mode(cardsContainer, input_handler);

	} else if (currentPage === "custom") {
        // Lógica específica do modo Personalizado
        reset_custom_mode(newGameContainer, input_handler);
    }
}

// Função específica para resetar modo personalizado
function reset_custom_mode(container, input_handler) {
    // Recreating input box (código original)
    const new_input = document.createElement("input");
    new_input.type = "text";
    new_input.className = "Input";
    new_input.placeholder = "Escreva aqui";
    new_input.autocomplete = "off";
    new_input.disabled = false;
    new_input.value = "";

    new_input.addEventListener("keydown", (event) => input_handler.input_on_keydown(event, new_input));
    new_input.addEventListener("input", (event) => input_handler.input_on_text_change(event, new_input));

    container.parentNode.replaceChild(new_input, container);

    // Reseting control variables
    input_handler.attempt_handler.number_attempts = 0;

    // Reseting attempt's counter
    if (input_handler.attempt_handler.div_attempts) {
        input_handler.attempt_handler.div_attempts.textContent = `${input_handler.attempt_handler.number_attempts}`;
    }
}

// Função específica para resetar modo True or False
function reset_tof_mode(container, input_handler) {
    // Remover div de "novo jogo" se existir
    const oldDiv = document.querySelector(".div_new_game");
    if (oldDiv) {
        oldDiv.remove();
    }

    // Reset das variáveis do True or False
    input_handler.current_game_session = null;
    input_handler.current_question_index = 0;
    
    // Reset do score display
    const scoreField = document.querySelector('.score-field');
    const currentField = document.querySelector('.current-question');
    const totalField = document.querySelector('.total-questions');
    
    if (scoreField) scoreField.textContent = '0';
    if (currentField) currentField.textContent = '0';
    if (totalField) totalField.textContent = '10';
    
    // Reabilitar botões de escolha
    const choiceButtons = document.querySelectorAll('.button_choice');
    choiceButtons.forEach(btn => btn.disabled = false);

    // Agora sim: iniciar novo jogo chamando a função da classe
    input_handler.start_new_tof_game().then(resultado => {
    	console.log("Resultado:", resultado);
	});
}