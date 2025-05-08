let selector = document.getElementsByName('filterType')[0];

selector.addEventListener("click", function(){
    let filterType = selector.value;
    
    let cuisineType = document.getElementsByName('cuisineTypes');
    let time = document.getElementById('cookTimeEl');
    let diff = document.getElementsByName('diff');

    if(filterType == 'title'){
        time.setAttribute('class', 'hidden');
        diff[0].setAttribute('class', 'hidden');
        cuisineType[0].setAttribute('class', 'hidden');
    }
    if(filterType == 'cuisineTypes'){
        cuisineType[0].removeAttribute('class');
        time.setAttribute('class', 'hidden');
        diff[0].setAttribute('class', 'hidden');
    }
    if(filterType == 'time'){
        time.removeAttribute('class');
        cuisineType[0].setAttribute('class', 'hidden');
        diff[0].setAttribute('class', 'hidden');
    }
    if(filterType == 'diff'){
        diff[0].removeAttribute('class');
        time.setAttribute('class', 'hidden');
        cuisineType[0].setAttribute('class', 'hidden');
    }
});
