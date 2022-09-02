const check = document.querySelectorAll(".driveDateBox input")

check[0].addEventListener("change", checkAll)

function checkAll(){
    if(check[0].checked){
        for(i=1; i<check.length; i++){
            check[i].checked = true
        }
    }else{
        for(i=1; i<check.length; i++){
            check[i].checked = false
        }
    }
}


for(i=1; i<check.length; i++){
    check[i].addEventListener("change", checkToAllcheck)
}

function checkToAllcheck(){
    if(check[1].checked == true && check[2].checked == true && check[3].checked == true && check[4].checked == true && check[5].checked == true && check[6].checked == true && check[7].checked == true){
        check[0].checked = true
    }else{
        check[0].checked = false
    }
}