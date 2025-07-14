/** 
 * @file frontend/site/scripts/hints.js
 * 
 * @author victorxaviercosta
 * @author HexagonalUniverse
 * 
 * @version 0.2
 */

import { render_hints, remove_hints_container } from "./renderer.js";
import { api } from "./api.js";

/** Handles backend hints request returning the backend's offered list of suggestions */
async function __get_backend_hints(input) {
    let response;
    try {
        response = await api("/guess/hint/", "POST", { "attempt": `${input}` });
		
    } catch(error) {
        console.log(error);
    }
    
    return response['closest_matches'];
}

/** Hides the hint's div element (Removing it) */
export function hide_hints(){
    remove_hints_container();
}

/** Display's the list of suggestions gotten from backend. */
export async function display_hints(user_input) {
    let hints = await __get_backend_hints(user_input);
    console.log(hints);
    render_hints(hints);
    
    return
}