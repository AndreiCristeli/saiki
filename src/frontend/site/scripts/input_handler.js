/** 
 * @file frontend/site/script/input_handler.js
 * 
 * @author AndreiCristeli
 * @author victorxaviercosta
 * 
 * @version 0.1
 */

import * as cl from "./attempt.js"


// TODO: Handle entity_type properly according to user's selection.
const ENTITY_TYPE_PH = "Algorithm"

// Normalizes user's input.
// Returns all input words captalized (Change as needed for the backend database).
function __normalize_input(input){
  let trimmed = input.trim(); // Removes leading and trailing spaces (but not spaces between words).
  return trimmed.toLowerCase();
}

// Envent handler for keydown on the input text box
export async function input_keydown(event, input, div_attempts) {
  const user_input = __normalize_input(event.target.value); 
  // console.log(`Nomalized Input: ${user_input}`);

  if (/^[a-zA-z]$/.test(event.key)){ // Using RegExp for validating if entry is a letter.
    // TODO: add suggestion logic.
    // console.log(event.key);
    
  } else if (event.key === 'Enter') {
    input.value = '';
    
    if(user_input) {
      let r = await cl.process_attempt(user_input, div_attempts, ENTITY_TYPE_PH);
      console.log("r" + r);
      if (r === -1){
        input.disabled = true;
        // Win Dialog.
      }
    }
  }
}

// Envent handler for click on the info button.
export function info_click(event, button) {
  const dialog = document.querySelector('.infoDialog');
  if (dialog) {
    dialog.showModal();
  }  
}

// Envent handler for click on the close button of the info dialog.
export function close_info_dialog(event, dialog) {
  if(dialog) {
    dialog.style.animation = 'desvanecer 0.8s ease-out forwards';

    dialog.addEventListener('animationend', function handleClose() {
      dialog.close();
      dialog.style.animation = '';
      dialog.removeEventListener('animationend', handleClose);
    });
  }
}  