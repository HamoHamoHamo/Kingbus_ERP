function deleteLetter() {
    for (i = 0; i < collectDateBox.length; i++) {
        let departure = collectDateBox[i].children[2].children[0].innerText.split("@")[0]
        let arrival = collectDateBox[i].children[2].children[1].innerText.split("@")[0]
        if (departure.length > 24) {
            collectDateBox[i].children[2].children[0].innerText = `${departure.substr(0, 24)} ... ▶`
        }else{
            collectDateBox[i].children[2].children[0].innerText = departure
        }
        if (arrival.length > 24) {
            collectDateBox[i].children[2].children[1].innerText = `${arrival.substr(0, 24)} ...`
        }else{
            collectDateBox[i].children[2].children[1].innerText = arrival
        }
    }
}

deleteLetter()