let selectEl = document.getElementById("addIngredients");
selectEl.addEventListener("click", addIngredients);

let textEl = document.getElementById("addInstructions");
textEl = addEventListener("click", addInstruction);

let ingContainer = document.getElementById("ingredientsForm");
function addIngredients(){
    let elToClone = document.getElementById("ingr");
    let clonedEl = elToClone.cloneNode(true);
    ingContainer.appendChild(clonedEl)
}

let insContainer = document.getElementById("instructionsForm");
function addInstruction(){
    let eltoClone = document.getElementById("inst");
    let clonedEl = eltoClone.cloneNode(true);
    insContainer.appendChild(clonedEl)
}
