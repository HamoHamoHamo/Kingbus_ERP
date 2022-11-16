function deleteLetter(){
    for (i = 0; i < collectDateBox.length; i++){
        collectDateBox[i].children[2].children[0].innerText = collectDateBox[i].children[2].children[0].innerText.split("<")[0]
        collectDateBox[i].children[2].children[1].innerText = collectDateBox[i].children[2].children[1].innerText.split("<")[0]
    };
}

deleteLetter()