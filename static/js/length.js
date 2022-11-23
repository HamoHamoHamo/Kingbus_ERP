const Title = document.querySelectorAll(".tableBody td a")

function lengthBreak(){
    for (i = 0; i < Title.length; i++){
        if(Title[i].innerText.length > 50){
            Title[i].innerText = `${Title[i].innerText.substr(0,47)} ...`
        }
    };
}

lengthBreak()