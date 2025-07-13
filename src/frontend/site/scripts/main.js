/** 
 * @file 	frontend/site/script/main.js
 * 
 * @author 	AndreiCristeli
 * @author 	victorxaviercosta
 * 
 * @version 0.1
 */

import * as ih from "./input_handler.js";
import { changeLanguage } from "./translate.js";
import { api } from "./api.js";
import { load_game_state_screen } from "./attempt.js"


// This function runs when the entire page (all HTML, CSS, sripts, images and resouces) is completely loaded.
window.onload = function () {
	window.addEventListener("pageshow", (event) => on_page_show(event));
	
	const input = document.querySelector('.Input');
	const div_attempts = document.querySelector('.attempts-field');
	input.addEventListener('keydown', (event) => ih.input_keydown(event, input, div_attempts));
	
	const button = document.querySelector('.footer-info');
	button.addEventListener('click', (event) => ih.info_click(event, button));
	
	const select_language = document.querySelector('.translateBox');
	select_language.addEventListener('change', (event) => changeLanguage(select_language.value));

	const closeBtn = document.querySelector('.closeDialog');
	if (closeBtn) {
		const dialog = document.querySelector('.infoDialog');
		closeBtn.addEventListener('click', (event) => ih.close_info_dialog(event, dialog));
	}
	
	// deletes the hint box when the input is out-of-focus.
  	document.querySelector(".Input").addEventListener('blur', function () {
	  let hints_container = document.querySelector(".hints");
      try {
          hints_container.remove();
          input_hint_div.removeChild(hints_container);
      } catch (NotFoundError) {
			
      }
  })
};

/**	Updates the visual information of the page, on load / refresh */
async function on_page_show(event) {
	/* ?
	if (event.persisted) {
		console.log("Loaded from cache");
	}
	*/
	
	let response;
	
    try {
        response = await api("/guess/load/", "POST", { "asd": "asd" });
		
    } catch(error) {

function updateContent() {
  	document.querySelector('.diaryText').textContent = i18next.t('diary');
  	document.querySelector('.trueOrFalseText').textContent = i18next.t('trueOrFalse');
  	document.querySelector('.customText').textContent = i18next.t('custom');
  	document.querySelector('h2').textContent = i18next.t('question');
  	document.querySelector('.Input').placeholder = i18next.t('inputPlaceholder');
  	document.querySelector('.attempts-label').textContent = i18next.t('attempts');

  	const labels = document.querySelectorAll('.hint-labels li');
  	const keys = [
    	'categoryInfoTitle',
    	'yearInfoTitle',
    	'timeInfoTitle',
    	'spaceInfoTitle',
    	'structureInfoTitle',
    	'solutionInfoTitle',
    	'generalityInfoTitle'
  	];

  	labels.forEach((el, idx) => {
    	el.textContent = i18next.t(keys[idx]);
  	});

  	document.querySelector('.howToPlayTitle').textContent = i18next.t('howToPlay');
  	document.querySelector('.howToPlayDesc').textContent = i18next.t('description');

  	document.querySelector('.categoryTitle').textContent = i18next.t('categoryInfoTitle');
  	document.querySelector('.categoryText').textContent = i18next.t('categoryInfoText');

  	document.querySelector('.yearTitle').textContent = i18next.t('yearInfoTitle');
  	document.querySelector('.yearText').textContent = i18next.t('yearInfoText');

  	document.querySelector('.timeTitle').textContent = i18next.t('timeInfoTitle');
  	document.querySelector('.timeText').textContent = i18next.t('timeInfoText');

  	document.querySelector('.spaceTitle').textContent = i18next.t('spaceInfoTitle');
  	document.querySelector('.spaceText').textContent = i18next.t('spaceInfoText');

  	document.querySelector('.structureTitle').textContent = i18next.t('structureInfoTitle');
  	document.querySelector('.structureText').textContent = i18next.t('structureInfoText');

  	document.querySelector('.solutionTitle').textContent = i18next.t('solutionInfoTitle');
  	document.querySelector('.solutionText').textContent = i18next.t('solutionInfoText');

  	document.querySelector('.generalityTitle').textContent = i18next.t('generalityInfoTitle');
  	document.querySelector('.generalityText').textContent = i18next.t('generalityInfoText');
}

function changeLanguage(lang) {
	i18next.changeLanguage(lang, () => {
    	updateContent();
  	});
}
        console.log(error);
    }
	
	// rendering it.
	load_game_state_screen(event, response);
	
    return response;
}	
