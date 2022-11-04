document.addEventListener("keydown", saveKeyPress)

function saveKeyPress(e){
    if(e.keyCode === 120){
        RouteList.submit();
    }
}