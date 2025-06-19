/** 
 * @file frontend/site/script/card_logic.js
 * 
 * @author AndreiCristeli
 * @author victorxaviercosta
 * 
 * @version 0.1
 */

//import { api } from "./api.js"

let attempts = 0; // Temporaly saved as a global shared variable.
// TODO: Structure a frontend Player data-structure.

import { render_card } from "./renderer.js"

async function __backend_attempt(entity_type, user_input){
    // Search in database passing entity_type and user_input.
    // Should return an JS object with information about the attempt.

    /* Not sure yet how should the backend call be.

    api("/hangar")
    .then(data => {
        communicate(data.msg);
    })
    .catch(err => console.error(err));
    */

    // Local json test.
    let response = await fetch("../script/test.json")
    let attempt = await response.json();
    
    // For now, returning random element from the test json file just for fun.
    // In practice it should be only one element returned from database.
    return attempt[Math.floor(Math.random() * 3)];
}

export async function process_attempt(user_input, div_attempts, entity_type){
    // Call back_end attempt process_logic.
    let attempt = await __backend_attempt(entity_type, user_input);

    // TODO: Treat invalid entry case.
    // Idea: Only call process_attempt if there's a 'first suggestion' when Suggestion is implemented.

    // Updating attempt count.
    attempts++;
    div_attempts.textContent = `${attempts}`;
    
    // Get player victory logic from backend.
    let card_class = `card ${attempt.type}`;
    console.log(`Card Class = ${card_class}`)

    // Add a new card corresponding to user's attempt.
    render_card(attempt, card_class);
}