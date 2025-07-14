/** 
 * @file frontend/site/scripts/attempt.js
 * 
 * @author AndreiCristeli
 * @author victorxaviercosta
 * @author HexagonalUniverse
 * 
 * @version 0.2
 */

import { api } from "./api.js"
import { input_keydown, new_game_click } from "./input_handler.js"; 
import { render_card, render_collection } from "./renderer.js"


export let number_attempts = 0; // Temporaly saved as a global shared variable.
// TODO: Structure a frontend Player data-structure.

/** Return Codes for the attempts processing */
export const ATTEMPT_RC = {
    SUCCESS: 0,         // Attempt successfully processed.
    REPEATED_ANSWER: 1, // The attempt is a repeated entry.
    NOT_FOUND: 2,       // Entity not found in db.
    VICTORY: 3,         // The attempt result's in player's Victory.
};

/** Updates the attempts count variable as well as the page's attempts counter element. */
function attempt_count_update(div_attempts) {
    ++ number_attempts;
    div_attempts.textContent = `${number_attempts}`;
}

/** Loads the attempt game state screen. 
    Called on page-show. */
export function load_game_state_screen(event, __on_load_response) {
    let div_attempts = document.querySelector('.attempts-field');
        
    render_collection(__on_load_response["entities"]);
	number_attempts = __on_load_response["tries"] - 1;

    attempt_count_update(div_attempts);
}

/** Executes a backend attempt request and gets it's response */
async function __backend_attempt(user_input, entity_type) {
    // Search in database passing entity_type and user_input.

    let attempt;
    try{
        attempt = await api("/guess/entity/", "POST", { entity : user_input });
    } catch(error){
        console.log(error);
    }

    return attempt;
}

/** Verifies possible  */
export function verify_repeat(user_input){
    const card_container = document.querySelector('.cards-container');
    
    // Sequentially verifying if there's any card matching user's input.
    for(let card of card_container.children){
        if(card.querySelector(".card-header").textContent.toLowerCase() === user_input){
            return true;
        }
    }

    return false;
}

/** Handles all the attempt processing logic. */
export async function process_attempt(user_input, div_attempts, entity_type){
    if (verify_repeat(user_input)){
        return ATTEMPT_RC.REPEATED_ANSWER;
    }

    let attempt = await __backend_attempt(user_input, entity_type);

    // Validating Backend's response.
    if(Object.keys(attempt).length === 0) {
        return ATTEMPT_RC.NOT_FOUND;
    }

    // TODO: Treat invalid entry case.
    // Idea: Only call process_attempt if there's a 'first suggestion' when Suggestion is implemented.

    // Incrementing attempts counter.
    attempt_count_update(div_attempts);

    // Adding a new card corresponding to user's attempt.
    render_card(attempt);

    // Validating player's victory.
    if (attempt.guessed === "correct") {
        return ATTEMPT_RC.VICTORY;
    }
    
    return ATTEMPT_RC.SUCCESS;
}

/** Handles the Player's win condition. */
export function win_condition(input) {
    input.disabled = true;
    
    /*
    Diary mode
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
    btn.addEventListener("click", (event) => new_game_click(event, btn));

    // Appending New Game's Button as a Child of New Game Div.
    div.appendChild(btn);
    input.parentNode.replaceChild(div, input);
}

/** Resets the Player's Game State in the frontend context. */
export function reset_game(container, div_attempts) {
    // Recreating input box.
    const new_input = document.createElement("input");
    new_input.type = "text";
    new_input.className = "Input";
    new_input.placeholder = "Escreva aqui";
    new_input.autocomplete = "off";
    new_input.disabled = false;
    new_input.value = "";

    new_input.addEventListener("keydown", (event) =>
        input_keydown(event, new_input, div_attempts)
    );

    container.parentNode.replaceChild(new_input, container);

    // Reseting control variables
    number_attempts = 0;

    // Reseting attempt's counter.
    if (div_attempts) {
        div_attempts.textContent = `${number_attempts}`;
    }

    // Removing all card elements from cards container.
    const cardsContainer = document.querySelector(".cards-container");
    if (cardsContainer) {
        cardsContainer.innerHTML = "";
    }
}
