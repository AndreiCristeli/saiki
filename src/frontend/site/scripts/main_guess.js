/** 
 * @file 	frontend/site/scripts/main.js
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

/** This function runs when the entire page (all HTML, CSS, sripts, images and resouces) is completely loaded.
 *  Basically Starts all the relevant Event Listener's logics to their respective HTML element.
 */
window.onload = function () {
	window.addEventListener("pageshow", (event) => on_page_show(event));
	
	const input = document.querySelector('.Input');
	const div_attempts = document.querySelector('.attempts-field');
	input.addEventListener('keydown', (event) => input_handler.input_keydown(event, input));
	
	const button = document.querySelector('.footer-info');
	button.addEventListener('click', (event) => input_handler.info_click(event, button));
	
	const select_language = document.querySelector('.translateBox');
	select_language.addEventListener('change', (event) => changeLanguage(select_language.value));

	const closeBtn = document.querySelector('.closeDialog');
	if (closeBtn) {
		const dialog = document.querySelector('.infoDialog');
		closeBtn.addEventListener('click', (event) => input_handler.close_info_dialog(event, dialog));
	}

	// Deletes the hint box when the input box is out-of-focus.
  	document.querySelector(".Input").addEventListener('blur', function () {
      try {
			input_handler.hints.hide();
      	} catch (NotFoundError) {
			// blank - No exception action needed.
      	}
  	})
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