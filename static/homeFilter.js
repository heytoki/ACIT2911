let selector = document.getElementsByName('filterType')[0];
selector.addEventListener("click", function(){
    let filterType = selector.value;
    
    let cuisineType = document.getElementsByName('cuisineTypes')[0];
    let time = document.getElementById('cookTimeEl');
    let diff = document.getElementsByName('diff')[0];

    if(filterType == 'title'){
        time.setAttribute('class', 'hidden');
        diff.setAttribute('class', 'hidden');
        cuisineType.setAttribute('class', 'hidden');
    }
    if(filterType == 'cuisineTypes'){
        cuisineType.removeAttribute('class');
        time.setAttribute('class', 'hidden');
        diff.setAttribute('class', 'hidden');
    }
    if(filterType == 'time'){
        time.removeAttribute('class');
        cuisineType.setAttribute('class', 'hidden');
        diff.setAttribute('class', 'hidden');
    }
    if(filterType == 'diff'){
        diff.removeAttribute('class');
        time.setAttribute('class', 'hidden');
        cuisineType.setAttribute('class', 'hidden');
    }
});
