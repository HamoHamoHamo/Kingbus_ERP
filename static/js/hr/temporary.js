const authority = document.querySelector(".PopupDataInputWork")

authority.addEventListener("change", temporarYuthority)

function temporarYuthority(){
    if(authority.options[authority.selectedIndex].value === "임시"){
        authorityDivision[0].style.display = "none"
        authorityDivision[1].style.display = "none"
    }else{
        authorityDivision[0].style.display = "block"
        authorityDivision[1].style.display = "flex"
    }
}
