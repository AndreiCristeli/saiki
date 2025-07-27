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

// TODO: Handle entity_type properly according to user's selection.
const ENTITY_TYPE_PH = "Algorithm"

export class InputHandler {
	constructor(renderer){
		this.hints = new Hints(renderer)
		this.attempt_handler = new AttemptsHandler(renderer)
	}
	
	// Normalizes user's input.
	// Returns all input words captalized (Change as needed for the backend database).
	#__normalize_input(input) {
		let trimmed = input.trim(); // Removes leading and trailing spaces (but not spaces between words).
		return trimmed.toLowerCase();
	}

	// Event handler for keydown on the input text box
	async input_keydown(event, input) {
		let user_input = this.#__normalize_input(event.target.value); 
		// console.log(`Nomalized Input: ${user_input}`);
	
		// In the case there's no input in the text-box
		if (!user_input){
			this.hints.hide();
			return;
		}
	
		if (/^[a-zA-z]$/.test(event.key)) { // Using RegExp for validating if entry is a letter.
			//console.log(event.key);
			this.hints.display(user_input);
	
		}else if (event.key == "ArrowUp") {
			console.log("arrowUp");
			this.hints.move_hint_selection("up");
			
		}else if (event.key == "ArrowDown") {
			console.log("arrowDown");
			this.hints.move_hint_selection("down");
		
		} else if (event.key === 'Enter') {
			if (this.hints.displaying){
				user_input = this.hints.the_hints[this.hints.selected_hint].toLowerCase();
			}

			this.hints.hide(); // Hinding the Hints
	
			  if (user_input === "milvus"){
				eg.showMilvusDialog(); input.value = ''; return;
	
			  } else if (user_input === "pokemon" || user_input === "monkepo"){
				eg.showPokemonDialog(); input.value = ''; return;
			  }
	
			let attempt_rc = await this.attempt_handler.process_attempt(user_input, ENTITY_TYPE_PH);
	
			switch (attempt_rc) {
				case ATTEMPT_RC.REPEATED_ANSWER: 
				case ATTEMPT_RC.NOT_FOUND:
					break;
				case ATTEMPT_RC.VICTORY: // Win Condition.
					win_condition(input, this);
	
				default:
					input.value = '';
			}
		}
	}

	// Event handler for when clicking on new game.
	new_game_click(event, btn) {
		const container = btn.closest(".div_new_game");
		reset_game(container, this);
	}

	// Event handler for click on the info button.
	info_click(event, button) {
		const dialog = document.querySelector('.infoDialog');
		if (dialog) {
			dialog.showModal();
		}  
	}

	// Event handler for click on the close button of the info dialog.
	close_info_dialog(event, dialog) {
		if(dialog) {
			dialog.style.animation = 'desvanecer 0.8s ease-out forwards';

			dialog.addEventListener('animationend', function handleClose() {
				dialog.close();
				dialog.style.animation = '';
				dialog.removeEventListener('animationend', handleClose);
			});
		}
	}  

	choice_click(event, button) { 
		console.log("Botão clicado:", button.textContent);
		if (button.textContent === "Verdá") {
			console.log("Você escolheu Verdadeiro.");
		} else {
			console.log("Você escolheu Falso.");
		}
	}
}



// TODO: rethink where these methods (win_condition and reset_game should go)

/** Handles the Player's win condition. */
function win_condition(input, input_handler) {
    input.disabled = true;
    
    /*
    Daily mode
    input.style.border = "2px solid green";
    input.style.backgroundColor = "#e0ffe0";
    input.style.color = "#004400";
    input.placeholder = "Parabéns! Você venceu! 🎉";
    */

    // Adding New Game Div Element.
    const div = document.createElement("div");
    div.textContent = "Parabéns! Você venceu! 🎉";
    div.className = "div_new_game";

    // Adding New Game Button.
    const btn = document.createElement("button");
    btn.textContent = "Novo Jogo";
    btn.className = "btn_new_game";
    btn.addEventListener("click", (event) => input_handler.new_game_click(event, btn));

    // Appending New Game's Button as a Child of New Game Div.
    div.appendChild(btn);
    input.parentNode.replaceChild(div, input);
}

/** Resets the Player's Game State in the frontend context. */
function reset_game(container, input_handler) {
    // Recreating input box.
    const new_input = document.createElement("input");
    new_input.type = "text";
    new_input.className = "Input";
    new_input.placeholder = "Escreva aqui";
    new_input.autocomplete = "off";
    new_input.disabled = false;
    new_input.value = "";

    new_input.addEventListener("keydown", (event) =>
        input_handler.input_keydown(event, new_input)
    );

    container.parentNode.replaceChild(new_input, container);

    // Reseting control variables
    input_handler.attempt_handler.number_attempts = 0;

    // Reseting attempt's counter.
    if (input_handler.attempt_handler.div_attempts) {
        input_handler.attempt_handler.div_attempts.textContent = `${input_handler.attempt_handler.number_attempts}`;
    }

    // Removing all card elements from cards container.
    const cardsContainer = document.querySelector(".cards-container");
    if (cardsContainer) {
        cardsContainer.innerHTML = "";
    }
}