document.addEventListener("keydown", saveKeyPress)

function saveKeyPress(e){
    if(e.keyCode === 113){
        RouteList.submit();
    }
}