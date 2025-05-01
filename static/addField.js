element = document.getElementById("addIngredients");
element.setAttribute(onclick, addIngredients());
element.addEventListener(onclick, addIngredients());

function addIngredients(){
    console.log('test');
}