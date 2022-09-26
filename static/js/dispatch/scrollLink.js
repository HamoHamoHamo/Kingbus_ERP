const scrollBox = document.querySelectorAll(".orderListSubScroll")
const scrollBoxAll = document.querySelector(".orderListScrollYBox")
const scrollBoxHeight = document.querySelector(".orderListScrollYBox div")
const scrollBoxTarget = document.querySelectorAll(".orderListScrollBox")
const mainContents = document.querySelectorAll(".orderListMain .orderListItem")
const subContents = document.querySelectorAll(".orderListSub .orderListItem")

scrollBox[0].addEventListener("scroll", moveCheck)
scrollBox[1].addEventListener("scroll", moveCheck)
scrollBoxAll.addEventListener("scroll", moveCheck)

function matchHeight() {
    scrollBoxHeight.style.height = `${scrollBoxTarget[0].offsetHeight * 0.1}rem`
}

function moveCheck(e) {
    scrollBox[0].scrollTop = e.target.scrollTop
    scrollBox[1].scrollTop = e.target.scrollTop
    scrollBoxAll.scrollTop = e.target.scrollTop
}


function listHeight() {
    for (i = 0; i < mainContents.length; i++) {
        if (mainContents[i].offsetHeight !== subContents[i].offsetHeight) {
            if (mainContents[i].offsetHeight > subContents[i].offsetHeight) {
                subContents[i].style.height = `${(mainContents[i].offsetHeight - 1) * 0.1}rem`
            } else {
                mainContents[i].style.height = `${(subContents[i].offsetHeight - 1) * 0.1}rem`
            }
        }
        for (j = 1; j < 19; j++) {
            subContents[i].children[j].style.height = `${subContents[i].children[0].offsetHeight * 0.1}rem`
        }
        mainContents[i].children[0].style.height = `${subContents[i].children[0].offsetHeight * 0.1}rem`
    }
}