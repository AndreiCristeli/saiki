/** 
 * @file frontend/site/scripts/renderer.js
 * 
 * @author victorxaviercosta
 * @author HexagonalUniverse
 * 
 * @version 0.1
 */

import { InputHandler } from "./input_handler.js"

export class Renderer {
	constructor(){
		this.input_handler = new InputHandler(this);
	}

	#render_katex(input_str, target_element) {
		katex.render(input_str, target_element, { 
			diplayMode: true, throwOnError: false
		});  
	}

	#render_math(field, input_list, target_element) {
		if (field === "average_time_complexity") {
			this.#render_katex("T \\in " + input_list, target_element);
		
		} else if (field === "auxiliary_space_complexity") {
			this.#render_katex("S \\in " + input_list, target_element);
		  
		} else {
			for (let value of input_list) {
			  target_element.textContent = target_element.textContent + `${value}\n`;
			}
		}
	}

	render_card(card_object) {
		/**
		 *  Card object must have the fields:
		 * 	name (string)
		 * 	guessed (string)
		 *  data ( {key (string): value (string)} )
		 */

		let card_class = `card ${card_object.guessed}`;
	
		// Creating the card div element.
		const card = document.createElement('div');
		card.className = card_class;
		
		// Creating the card header div element.
		const header = document.createElement('div');
		header.className = "card-header";
		header.textContent = card_object.name;
		card.appendChild(header);
		
		// Creating infoGrid div element.
		const infoGrid = document.createElement('div');
		infoGrid.className = 'info-grid';
		
		// Adding attributes elements.
		for (let key in card_object.data) {
			const infoItem = document.createElement('div');
			
			infoItem.className = `info-item ${card_object.data[key][1]}-color`;
			
			this.#render_math(key, card_object.data[key][0], infoItem);
			infoGrid.appendChild(infoItem);
		}
		
		// Adding info-grid to card
		card.appendChild(infoGrid);
		
		// Insert the card to body ou em outro container (ex: abaixo do último card)
		const container = document.querySelector('.cards-container');
		container.insertBefore(card, container.firstChild);
	}

	remove_hints_container(input_hint_div) {
		let hints_container = document.querySelector(".hints");
	
		if (hints_container) { 
			try {
				hints_container.remove();
				//input_hint_div.removeChild(hints_container);

			} catch (NotFoundError) {
				console.log(`[ERROR]: Unnable to remove hints container: \n ${NotFoundError}`);
			}
		}
	}

	/** Renders the hints at the input text-box. */
	render_hints(hints, selected) {
		const input_hint_div = document.querySelector(".input-hint");
		
		this.remove_hints_container(input_hint_div);
		
		if (hints.length == 0)
			return;
		
		// re-creating hints container.
		let hints_container = document.createElement('div');
		hints_container.className = "hints"

		// console.log(`selected = ${selected}`);
		
		// adding each hint row.
		for (let name of hints) {
			// each hint row...
			const hint_item = document.createElement('div');
			hint_item.className = "hint_item";

			if (name == hints[selected]) {
				hint_item.className = hint_item.className + " selected";
				// console.log(`selected name = ${name}`);
			}

			hint_item.innerText = name;
			hint_item.addEventListener('click', (event) => this.input_handler.hint_click(event, hint_item));
			// hint_item.addEventListener('touchend', (event) => this.input_handler.hint_click(event, hint_item));
			hint_item.addEventListener('mouseenter', (event) => {
    			hint_item.className = hint_item.className + " selected";
			});
			hint_item.addEventListener('mouseleave', (event) => {
    			hint_item.className = "hint_item";
			});
			hints_container.appendChild(hint_item);
		}
		
		input_hint_div.appendChild(hints_container);
	}

	update_hints(hints, selected){
		const hints_container = document.querySelector('.hints');
		// console.log(`Updating hints container`);

		// adding each hint row.
		for (let child of hints_container.childNodes) {
			// each hint row...
			child.className = "hint_item";
			
			if (child.innerText == hints[selected]) {
				child.className = child.className + " selected"
				// console.log(`new selected name = ${child.innerText}`);
			}
		}
	}

	/** Bulk-loads a collection of entities.
	 *  Used on page-refresh, for maintaining the visual information of the game-state. */
	render_collection(entities) {
		// console.log("entities:", entities);
	
		// iteratively rendering each card, in order...
		for (let entity of entities) {
			this.render_card(entity);
		}
	}


	// Adicionar à classe Renderer

	// Renderizar questões do True or False
	render_tof_questions(questions) {
		
		const container = document.querySelector('.cards-container');
		
		if (!container) {
			console.error('Container .cards-container não encontrado!');
			return;
		}

		container.innerHTML = ''; // Limpar container
		
		questions.forEach((question, index) => {
			this.render_tof_card(question, index);
		});
	}

	// Renderizar card de questão True or False
	render_tof_card(question, index) {
		console.log('Question object:', question);
		
		const card = document.createElement('div');
		card.className = 'algorithm-card';
		card.id = `tof-card-${index}`;
		
		card.innerHTML = `
			<div class="card-header">
				<div class="algorithm-name">${question.area}</div>
			</div>

			<div class="card-content">
				<div class="info-row">
					<span class="info-label">Pergunta:</span>
					<span class="info-value">${question.question}</span>
				</div>
			</div>
			<div class="user-answer">
				<button class="answer-btn true-btn" data-question="${index}" data-answer="true">
					Verdadeiro
				</button>
				<button class="answer-btn false-btn" data-question="${index}" data-answer="false">
					Falso
				</button>
			</div>
		`;
		
		// Adicionar event listeners para botões individuais
		const answerBtns = card.querySelectorAll('.answer-btn');
		answerBtns.forEach(btn => {
			btn.addEventListener('click', (e) => {
				const questionIndex = parseInt(e.target.dataset.question);
				const answer = e.target.dataset.answer === 'true';
				// this.input_handler.submit_answer(questionIndex, answer);
				this.input_handler.process_global_tof_answer(answer);
			});
		});
		
		const container = document.querySelector('.cards-container');
		container.appendChild(card);
	}

	// Atualizar UI da questão após resposta
	update_tof_question_ui(questionIndex, isCorrect, userAnswer, correctAnswer) {
		const card = document.getElementById(`tof-card-${questionIndex}`);
		if (!card) return;
		
		const buttons = card.querySelectorAll('.answer-btn');
		
		// Desabilitar todos os botões
		buttons.forEach(btn => btn.disabled = true);
		
		buttons.forEach(btn => {
			const btnAnswer = btn.dataset.answer === 'true';
			
			// Marcar resposta do usuário
			if (btnAnswer === userAnswer) {
				btn.classList.add(isCorrect ? 'correct' : 'incorrect');
			}
			
			// Sempre mostrar a resposta correta
			if (btnAnswer === correctAnswer) {
				btn.classList.add('correct');
			}
		});
		
		// Adicionar classe ao card para indicar que foi respondido
		card.classList.add('answered');
		if (isCorrect) {
			card.classList.add('correct-answer');
		} else {
			card.classList.add('incorrect-answer');
		}
	}

	// Criar botão "Novo Jogo"
	create_new_game_button(containerSelector = "body") {
		// Verifica se já existe um botão para não duplicar
		// let existingBtn = document.querySelector(".new-game-btn");
		// if (existingBtn) {
		// 	console.warn("Botão Novo Jogo já existe.");
		// 	return existingBtn;
		// }

		// Criar botão
		const newGameBtn = document.createElement("button");
		newGameBtn.className = "new-game-btn";
		newGameBtn.id = "new-game-btn";
		newGameBtn.textContent = "Novo Jogo";

		// Adicionar ao container
		const container = document.querySelector(containerSelector);
		if (!container) {
			console.error("Container para o botão não encontrado:", containerSelector);
			return null;
		}
		container.appendChild(newGameBtn);

		// Registrar evento de clique
		newGameBtn.addEventListener("click", async () => {
			console.log("Clique detectado no botão Novo Jogo!");
			try {
				await this.input_handler.start_new_tof_game();
			} catch (e) {
				console.error("Erro ao iniciar novo jogo:", e);
			}
		});

		return newGameBtn;
	}

}