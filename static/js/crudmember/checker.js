const popupAreaModules = document.querySelectorAll(".popupAreaModules")
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const checkerCloseBtn = document.querySelector(".checkerCloseBtn")
const checkDateData = document.querySelector(".checkDateData")
const checkerDataBox = document.querySelectorAll(".checkerDataBox")

window.onload = function () {
    const checkMark = document.querySelectorAll(".checkMark")

    let parms = new URLSearchParams(location.search)
    let finishedCheck = []

    if (!parms.has("change")) {
        for (i = 0; i < checkList.length; i++) {
            if (checkList[i] !== "") {
                finishedCheck.push(i)
            }
        };

        for (i = 0; i < finishedCheck.length; i++) {
            checkMark[finishedCheck[i]].children[0].style.fill = "#59C8AA"
        };


        for (i = 0; i < checkMark.length; i++) {
            checkMark[i].addEventListener("click", openChecker)
        };
    }else{
        drawOrder()
    }

    const scheduleList = document.querySelectorAll(".dataCellCalender")


    for (i = 0; i < scheduleList.length; i++) {
        scheduleList[i].addEventListener("click", openScheduleList)
    };


    const calnderItem = document.querySelectorAll(".calnderItem")
    sliceLength(calnderItem)
}



popupBgModules[0].addEventListener("click", closeChecker)
SidemenuUseClose.addEventListener("click", closeChecker)
checkerCloseBtn.addEventListener("click", closeChecker)

function closeChecker() {
    popupAreaModules[0].style.display = "none"
}

function openChecker() {
    popupAreaModules[0].style.display = "block"

    checkerDataBox[0].innerText = checkList[this.parentNode.parentNode.children[0].children[0].innerText - 1].creator
    checkerDataBox[1].innerText = checkList[this.parentNode.parentNode.children[0].children[0].innerText - 1].date

    if(checkerDataBox[0].innerText === "undefined"){
        checkerDataBox[0].innerText = ""
    }

    if(checkerDataBox[1].innerText === "undefined"){
        checkerDataBox[1].innerText = ""
    }

    let dataTitle = ""
    if (this.parentNode.parentNode.children[0].children[0].innerText < 10) {
        dataTitle = `${dateTitle.innerText.replace(/\년 /g, "-").split("월")[0]}-0${this.parentNode.parentNode.children[0].children[0].innerText}`
    } else {
        dataTitle = `${dateTitle.innerText.replace(/\년 /g, "-").split("월")[0]}-${this.parentNode.parentNode.children[0].children[0].innerText}`
    }
    checkDateData.value = dataTitle
}