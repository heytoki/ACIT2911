let ingContainer = document.getElementById("ingredientsForm");
function addIngredient(){
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

function remInstruction() {
    var element = document.getElementById('instructionsForm');
    var nested = element.getElementsByTagName('li');
    if(nested.length > 1){
        element.removeChild(nested[nested.length - 1]);
    }
}

function remIngredient() {
    var element = document.getElementById('ingredientsForm');
    var nested = element.getElementsByTagName('li');
    if(nested.length > 1){
        element.removeChild(nested[nested.length - 1]);
    }
}

function popUp(){
    window.open(
        '/ingredient',
        '_blank'
    );
}