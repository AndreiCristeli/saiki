/** 
 * @file frontend/site/scripts/renderer.js
 * 
 * @author victorxaviercosta
 * @author HexagonalUniverse
 * 
 * @version 0.1
 */

function render_katex(input_str, target_element) {
    katex.render(input_str, target_element, { 
      diplayMode: true, throwOnError: false
    });  
}

function render_math(field, input_list, target_element) {

    if (field === "average_time_complexity") {
        render_katex("T \\in " + input_list, target_element);
      
    } else if (field === "auxiliary_space_complexity") {
        render_katex("S \\in " + input_list, target_element);
      
    } else {
        for (let value of input_list) {
          target_element.textContent = target_element.textContent + `${value}\n`;
        }
    }
}

export function render_card(object) {
  let card_class = `card ${object.guessed}`;

  // Creating the card div element.
  const card = document.createElement('div');
  card.className = card_class;
  
  // Creating the card header div element.
  const header = document.createElement('div');
  header.className = "card-header";
  header.textContent = object.name;
  card.appendChild(header);

  // Creating infoGrid div element.
  const infoGrid = document.createElement('div');
  infoGrid.className = 'info-grid';

  // Adding attributes elements.
  for (let key in object.data) {
    const infoItem = document.createElement('div');
    
    infoItem.className = `info-item ${object.data[key][1]}-color`;
    
    render_math(key, object.data[key][0], infoItem);
    infoGrid.appendChild(infoItem);
  }

  // Adding info-grid to card
  card.appendChild(infoGrid);
  
  // Insert the card to body ou em outro container (ex: abaixo do último card)
  const container = document.querySelector('.cards-container');
  container.insertBefore(card, container.firstChild);
}

export function remove_hints_container() {
  let hints_container = document.querySelector(".hints");

  if (hints_container) { 
    try {
        hints_container.remove();
        input_hint_div.removeChild(hints_container);
    } catch (NotFoundError) {
        
    }
  }
}

/** Renders the hints at the input text-box. */
export function render_hints(hints) {

  const input_hint_div = document.querySelector(".input-hint");
  
  remove_hints_container();

  if (hints.length == 0)
    return;
  
  // re-creating hints container.
  let hints_container = document.createElement('div');
  hints_container.className = "hints"

  // * @TODO organize it.
  
  // adding each hint row.
  for (let name of hints) {
    // each hint row...
    const hint_item = document.createElement('div');
    hint_item.className = "hint_item";
    hint_item.innerText = name;
    hints_container.appendChild(hint_item);
  }
  
  input_hint_div.appendChild(hints_container);
}

/** Bulk-loads a collection of entities.
 *  Used on page-refresh, for maintaining the visual information of the game-state. */
export function render_collection(entities) {
    // console.log("entities:", entities);
  
    // iteratively rendering each card, in order...
    for (let entity of entities) {
      render_card(entity);
    }
}
