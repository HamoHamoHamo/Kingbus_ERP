const age = document.querySelectorAll(".tableBody td:nth-child(4)")

function ageCalculator() {
    let now = new Date();
    let year = now.getFullYear();
    var month = now.getMonth() + 1;
    var date = now.getDate();
    for (i = 0; i < regDatas.length; i++) {
        if (regDatas[i].birthdate.substr(4, 2) < month) {
            age[i].innerText = `${year - regDatas[i].birthdate.substr(0, 4) + 1}(${year - regDatas[i].birthdate.substr(0, 4)})`
        } else if (regDatas[i].birthdate.substr(4, 2) == month) {
            if (regDatas[i].birthdate.substr(6, 2) <= date) {
                age[i].innerText = `${year - regDatas[i].birthdate.substr(0, 4) + 1}(${year - regDatas[i].birthdate.substr(0, 4)})`
            } else {
                age[i].innerText = `${year - regDatas[i].birthdate.substr(0, 4) + 1}(${year - regDatas[i].birthdate.substr(0, 4) - 1})`
            }
        } else {
            age[i].innerText = `${year - regDatas[i].birthdate.substr(0, 4) + 1}(${year - regDatas[i].birthdate.substr(0, 4) - 1})`
        }
    }
}

ageCalculator()