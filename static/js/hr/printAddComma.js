const printComma = document.querySelectorAll(".printComma")

function printAddComma(){
    for (i = 0; i < printComma.length; i++){
        printComma[i].innerText = printComma[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };    
}

printAddComma()