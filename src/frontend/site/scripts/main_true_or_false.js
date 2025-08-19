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

let renderer = new Renderer()

// Adicionar após as importações
let gameSession = null;
let currentQuestionIndex = 0;

window.onload = function () {
    const currentPage = document.body.dataset.page;

    const menuItems = document.querySelectorAll(".menu-item");
    menuItems.forEach(item => {
        if (item.dataset.page === currentPage) {
            item.classList.add("active");
        } else {
            item.classList.remove("active");
        }
    });

    // Info button
    const button = document.querySelector('.footer-info');
    button.addEventListener('click', (event) => renderer.input_handler.info_click(event, button));

    // Choice buttons (Verdadeiro/Falso)
    // const buttons = document.querySelectorAll('.button_choice');
    // buttons.forEach(button => {
    //     button.addEventListener('click', (event) => renderer.input_handler.choice_click(event, button));
    // });

    // Close dialog button
    const closeBtn = document.querySelector('.closeDialog');
    if (closeBtn) {
        const dialog = document.querySelector('.infoDialog');
        closeBtn.addEventListener('click', (event) => renderer.input_handler.close_info_dialog(event, dialog));
    }

    // New game button
    // const newGameBtn = document.querySelector('.new-game-btn');
    // console.log("Botão encontrado?", newGameBtn);

    // if (newGameBtn) {
    //   newGameBtn.addEventListener('click', async () => {
    //     console.log("Clique detectado!");
    //     try {
    //       await initializeGame();
    //     } catch (e) {
    //       console.error("Erro ao iniciar novo jogo:", e);
    //     }
    //   });
    // } else {
    //   console.warn("Botão '.new-game-btn' não encontrado no DOM!");
    // }


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