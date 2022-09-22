const scrollBox = document.querySelectorAll(".orderListSubScroll")
const scrollBoxAll = document.querySelector(".orderListScrollYBox")
const scrollBoxHeight = document.querySelector(".orderListScrollYBox div")
const scrollBoxTarget = document.querySelectorAll(".orderListScrollBox")

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