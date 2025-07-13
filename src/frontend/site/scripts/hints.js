import { render_hints, remove_hints_container } from "./renderer.js";
import { api } from "./api.js";

// Should Retur a list of Names of the specified entity
async function __get_backend_hints(input) {
    let response;
    try {
        response = await api("/guess/hint/", "POST", { "attempt": `${input}` });
		
    } catch(error) {
        console.log(error);
    }
    
    return response['closest_matches'];
}

export function hide_hints(){
    remove_hints_container();
}

export async function display_hints(user_input) {
    let hints = await __get_backend_hints(user_input);
    console.log(hints);
    render_hints(hints);
    
    return
}