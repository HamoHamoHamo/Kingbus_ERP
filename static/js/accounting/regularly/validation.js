function validation(){
    for (i = 0; i < collectDateBox.length; i++){
        collectDateBox[i].children[3].innerText = collectDateBox[i].children[3].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        collectDateBox[i].children[4].innerText = collectDateBox[i].children[4].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        collectDateBox[i].children[5].innerText = collectDateBox[i].children[5].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        collectDateBox[i].children[6].innerText = collectDateBox[i].children[6].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        collectDateBox[i].children[7].innerText = collectDateBox[i].children[7].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        collectDateBox[i].children[10].innerText = collectDateBox[i].children[10].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };
}

validation()