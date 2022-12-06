const btnBox = document.querySelector(".btnBox")

function authorityNotice(){
    if(AUTHORITY >= 3){
        btnBox.style.display = "none"
    }
}
authorityNotice()