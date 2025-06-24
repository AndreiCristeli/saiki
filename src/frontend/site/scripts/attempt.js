/** 
 * @file frontend/site/script/card_logic.js
 * 
 * @author AndreiCristeli
 * @author victorxaviercosta
 * 
 * @version 0.1
 */

import { api } from "./api.js"

let attempts = 0; // Temporaly saved as a global shared variable.
let victory = false; // Temporaly saved as a global shared variable.
// TODO: Structure a frontend Player data-structure.

import { render_card } from "./renderer.js"

async function __backend_attempt(user_input, entity_type){
    // Search in database passing entity_type and user_input.

    let attempt;
    try{
        attempt = await api("/guess/entity/", "POST", { entity : user_input });
    } catch(error){
        console.log(error);
    }

    return attempt;
}

export function verify_repeat(user_input){
    const card_container = document.querySelector('.cards-container');

    for(let card of card_container.children){
        if(card.querySelector(".card-header").textContent.toLowerCase() === user_input){
            return true;
        }
    }

    return false;
}

export async function process_attempt(user_input, div_attempts, entity_type){
    if (verify_repeat(user_input)){
        return -1;
    }

    // Call back_end attempt process_logic.
    let attempt = await __backend_attempt(user_input, entity_type);
    if(Object.keys(attempt).length === 0) {
        return -2; // Entity not found in db.
    }

    // TODO: Treat invalid entry case.
    // Idea: Only call process_attempt if there's a 'first suggestion' when Suggestion is implemented.

    // Updating attempt count.
    attempts++;
    div_attempts.textContent = `${attempts}`;
    
    // Get player victory logic from backend.
    let card_class = `card ${attempt.type}`;
    console.log(`Card Class = ${card_class}`);

    // Add a new card corresponding to user's attempt.
    
    render_card(attempt, card_class);

    if(attempt.type === "correct"){
        victory = true;
        return -3;
    }

    return 0;
}