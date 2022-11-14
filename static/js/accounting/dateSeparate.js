const depositCell = document.querySelectorAll(".depositCell")
const depositTbody = document.querySelector(".depositTbody")

function separating(unprocessed, processed, deleteCheck) {

    //option에 따른 구분
    let optionArr = []
    for (i = 0; i < depositCell.length; i++) {
        if (unprocessed && processed && depositCell[i].children[9].innerText === "미처리" || depositCell[i].children[9].innerText === "완료") {
            optionArr.push(depositCell[i])
        } else if (unprocessed && !processed && depositCell[i].children[9].innerText === "미처리") {
            optionArr.push(depositCell[i])
        } else if (!unprocessed && processed && depositCell[i].children[9].innerText === "완료") {
            optionArr.push(depositCell[i])
        } else if (deleteCheck) {
            optionArr = []
        }
    };

    //초기화
    for (i = 0; i < depositTbody.children.length; i++) {
        if (!depositTbody.children[i].classList.contains("depositCell")) {
            depositTbody.children[i].remove();
        }
    };

    //생성
    for (i = 0; i < optionArr.length; i++) {
        if (i < optionArr.length - 1) {
            if (optionArr[i].children[2].innerText.split(" ")[0] !== optionArr[i + 1].children[2].innerText.split(" ")[0]) {
                const total = document.createElement("tr")
                total.setAttribute("class", "dayTotal")
                total.setAttribute("class", "dayTotal")
                optionArr[i].after(total)
                const tatalDateTd = document.createElement("td")
                tatalDateTd.setAttribute("colspan", "6")
                tatalDateTd.innerText = `${optionArr[i].children[2].innerText.substr(0, 4)}.${optionArr[i].children[2].innerText.substr(5, 2)}.${optionArr[i].children[2].innerText.substr(8, 2)}`
                total.appendChild(tatalDateTd)
                for (j = 0; j < 4; j++) {
                    const tatalTd = document.createElement("td")
                    total.appendChild(tatalTd)
                };
            }
        } else if (i === optionArr.length - 1) {
            const total = document.createElement("tr")
            total.setAttribute("class", "dayTotal")
            optionArr[i].after(total)
            const tatalDateTd = document.createElement("td")
            tatalDateTd.setAttribute("colspan", "6")
            tatalDateTd.innerText = `${optionArr[i].children[2].innerText.substr(0, 4)}.${optionArr[i].children[2].innerText.substr(5, 2)}.${optionArr[i].children[2].innerText.substr(8, 2)}`
            total.appendChild(tatalDateTd)
            for (j = 0; j < 4; j++) {
                const tatalTd = document.createElement("td")
                total.appendChild(tatalTd)
            };
        }
    };
}

separating();