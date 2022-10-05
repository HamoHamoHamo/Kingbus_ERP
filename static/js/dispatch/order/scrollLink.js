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
        if (subContents[i].children[0].clientHeight >= 50) {
            mainContents[i].children[0].style.height = `${(subContents[i].children[0].clientHeight + 4) * 0.1}rem`
            mainContents[i].children[1].style.height = `${(subContents[i].children[0].clientHeight + 4) * 0.1}rem`
            for (j = 0; j < subContents[i].children.length; j++) {
                subContents[i].children[j].style.height = `${(subContents[i].children[0].clientHeight + 2) * 0.1}rem`
            }
        } else {
            mainContents[i].children[0].style.height = "5.2rem"
            mainContents[i].children[1].style.height = "5.2rem"
            for (j = 0; j < subContents[i].children.length; j++) {
                subContents[i].children[j].style.height = "5.2rem"
            }
        }
    }
}