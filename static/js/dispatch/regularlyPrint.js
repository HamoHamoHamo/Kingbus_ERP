const listItme = document.querySelectorAll(".listItme")

function sort() {
    for (i = 0; i < listItme.length; i++) {
        if(listItme[i].children[1].innerText !== ""){
            listItme[i].classList.add("haveDispatch")
        }
    };
    for (i = 0; i < listItme.length; i++){
        if(!listItme[i].classList.contains("haveDispatch")){
            const copyItme = listItme[i].cloneNode(true)
            listItme[i].parentNode.appendChild(copyItme)
            listItme[i].remove()
        }
    };
}

sort()
