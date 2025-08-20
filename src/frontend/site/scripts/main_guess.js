/** 
 * @file 	frontend/site/scripts/main.js
 * 
 * @author 	AndreiCristeli
 * @author 	victorxaviercosta
 * 
 * @version 0.2
 */

import { Renderer } from "./renderer.js";
import { changeLanguage } from "./translate.js";
import { api } from "./api.js";

/**
 *  Structure:
 * 		Renderer {
 *			InputHandler {
 * 				AttemptsHandler -> <Renderer>
 * 				Hints -> <Renderer>
 * 			}
 * 		}
 */

let renderer = new Renderer()

/** This function runs when the entire page (all HTML, CSS, sripts, images and resouces) is completely loaded.
 *  Basically Starts all the relevant Event Listener's logics to their respective HTML element.
 */
window.onload = function () {
	window.addEventListener("pageshow", (event) => on_page_show(event));
	const currentPage = document.body.dataset.page;

	const menuItems = document.querySelectorAll(".menu-item");

	menuItems.forEach(item => {
		if (item.dataset.page === currentPage) {
			item.classList.add("active");
		} else {
			item.classList.remove("active"); // útil se for SPA
		}
	});

	const input = document.querySelector('.Input');
	const div_attempts = document.querySelector('.attempts-field');
	input.addEventListener('input', (event) => renderer.input_handler.input_on_text_change(event));
	input.addEventListener('keydown', (event) => renderer.input_handler.input_on_keydown(event));
	
	const button = document.querySelector('.footer-info');
	button.addEventListener('click', () => renderer.input_handler.info_click());
	
	const select_language = document.querySelector('.translateBox');
	select_language.addEventListener('change', () => changeLanguage(select_language.value));

	const nav_logout = document.querySelector(".logout-btn");
	nav_logout.addEventListener("click", () => renderer.input_handler.logout_click());

	const closeBtn = document.querySelector('.closeDialog');
	if (closeBtn) {
		const dialog = document.querySelector('.infoDialog');
		closeBtn.addEventListener('click', () => renderer.input_handler.close_info_dialog(dialog));
	}

	// Deletes the hint box when the input box is out-of-focus.
	document.querySelector(".Input").addEventListener('blur', () => {
		setTimeout(() => {
			try {
				renderer.input_handler.hints.hide();
				console.log("BLUR");
			} catch (NotFoundError) {
				// blank - No exception action needed.
			}
		}, 120);
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
	renderer.input_handler.attempt_handler.load_game_state_screen(event, response);

  return response;
}	