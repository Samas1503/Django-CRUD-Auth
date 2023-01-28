function mostrarCheck() {
    var check = document.querySelector('#important');
    var toggle = document.getElementById('toggle');
    if (check.checked === false){
        toggle.classList.remove('bi-toggle-off');
        toggle.classList.add('bi-toggle-on');
    }
    else {
        toggle.classList.remove('bi-toggle-on');
        toggle.classList.add('bi-toggle-off');
    }
}