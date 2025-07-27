/** 
 * @file 	frontend/site/scripts/main_true_or_false.js
 * 
 * @author 	AndreiCristeli
 * @author 	victorxaviercosta
 * 
 * @version 0.2
 */

import { InputHandler } from "./input_handler.js";
import { Renderer } from "./renderer.js";
import { changeLanguage } from "./translate.js";
import { api } from "./api.js";

/**
 *  Structure:
 * 		InputHandler {
 * 			AttemptsHandler -> <Renderer>
 * 			Hints -> <Renderer>
 * 		}
 * 
 */

let renderer = new Renderer()
let input_handler = new InputHandler(renderer)
console.log("Página carregada: eventos sendo registrados.");
/** This function runs when the entire page (all HTML, CSS, sripts, images and resouces) is completely loaded.
 *  Basically Starts all the relevant Event Listener's logics to their respective HTML element.
 */
window.onload = function () {
  window.addEventListener("pageshow", (event) => on_page_show(event));

  const button = document.querySelector('.footer-info');
	button.addEventListener('click', (event) => input_handler.info_click(event, button));

  const buttons = document.querySelectorAll('.button_choice');
  buttons.forEach(button => {
    button.addEventListener('click', (event) => input_handler.choice_click(event, button));
  });

  const closeBtn = document.querySelector('.closeDialog');
  if (closeBtn) {
    const dialog = document.querySelector('.infoDialog');
    closeBtn.addEventListener('click', (event) => input_handler.close_info_dialog(event, dialog));
  }

};

/**	Updates the visual information of the page, on load / refresh */
async function on_page_show(event) {
  let response;
  
    try {
        response = await api("/guess/load/", "POST", { "asd": "asd" });
    
    } catch(error) {
        console.log(error);
    }
  
  // Rendering it.
  input_handler.attempt_handler.load_game_state_screen(event, response);
  
    return response;
}	