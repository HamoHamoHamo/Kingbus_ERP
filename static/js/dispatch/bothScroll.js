const scrollBox = document.querySelectorAll(".scrollListTableWidth")
const copyScrollY = document.querySelectorAll(".ListTableBox")

scrollBox[1].addEventListener("scroll", moveCheck)

function moveCheck(e) {
    copyScrollY[1].scrollTop = e.target.scrollTop
    scrollBox[0].scrollLeft = e.target.scrollLeft
}