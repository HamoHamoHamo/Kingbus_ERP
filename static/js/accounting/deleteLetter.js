function deleteLetter() {
    for (i = 0; i < collectDateBox.length; i++) {
        if (collectDateBox[i].children[2].children[0].innerText.length > 24) {
            collectDateBox[i].children[2].children[0].innerText = `${collectDateBox[i].children[2].children[0].innerText.substr(0, 24)} ... ▶`
        }
        if (collectDateBox[i].children[2].children[1].innerText.length > 24) {
            collectDateBox[i].children[2].children[1].innerText = `${collectDateBox[i].children[2].children[1].innerText.substr(0, 24)} ...`
        }
    }
}

deleteLetter()