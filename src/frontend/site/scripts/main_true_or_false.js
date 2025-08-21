/** 
 * @file 	frontend/site/scripts/main_true_or_false.js
 * 
 * @author 	AndreiCristeli
 * @author 	victorxaviercosta
 * 
 * @version 0.2
 */

import { Renderer } from "./renderer.js";
import { api } from "./api.js";
import { changeLanguage } from "./translate.js";

let renderer = new Renderer()

// Adicionar após as importações
let gameSession = null;

window.onload = function () {
    const currentPage = document.body.dataset.page;

	const menuItems = document.querySelectorAll(".menu-item");
  
	menuItems.forEach(item => {
    if (item.dataset.page === currentPage) {
      item.classList.add("active");
		} else {
      item.classList.remove("active"); // útil se for SPA
		}
	});
  
    const nav_logout = document.querySelector(".logout-btn");
    nav_logout.addEventListener("click", () => renderer.input_handler.logout_click());

    // Info button
    const button = document.querySelector('.footer-info');
    button.addEventListener('click', (event) => renderer.input_handler.info_click(event, button));

    // Close dialog button
    const closeBtn = document.querySelector('.closeDialog');
    if (closeBtn) {
        const dialog = document.querySelector('.infoDialog');
        closeBtn.addEventListener('click', (event) => renderer.input_handler.close_info_dialog(event, dialog));
    }

    const select_language = document.querySelector('.translateBox');
    select_language.addEventListener('change', (event) => changeLanguage(select_language.value));

    // Inicializar jogo automaticamente
    initializeGame();
};

async function initializeGame() {
    try {
        await renderer.input_handler.start_new_tof_game();
    } catch (error) {
        console.error('Erro ao inicializar jogo:', error);
    }
}