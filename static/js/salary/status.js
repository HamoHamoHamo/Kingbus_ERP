const scrollBox = document.querySelector(".orderListSubScroll")
const scrollBoxAll = document.querySelector(".orderListScrollYBox")
const scrollBoxHeight = document.querySelector(".orderListScrollYBox div")
const scrollBoxTarget = document.querySelectorAll(".orderListScrollBox")
const mainContents = document.querySelectorAll(".orderListMain .orderListItem")
const subContents = document.querySelectorAll(".orderListSub .orderListItem")

scrollBox.addEventListener("scroll", moveCheck)
scrollBoxAll.addEventListener("scroll", moveCheck)


function moveCheck(e) {
    scrollBox.scrollTop = e.target.scrollTop
    scrollBoxAll.scrollTop = e.target.scrollTop
}


// function listHeight() {
//     for (i = 0; i < mainContents.length; i++) {
//         let heightArr = []
//         for (j = 0; j < mainContents[i].children.length; j++) {
//             heightArr.push(mainContents[i].children[j].clientHeight)
//         };
//         for (j = 0; j < subContents[i].children.length; j++) {
//             heightArr.push(subContents[i].children[j].clientHeight)
//         };
//         heightArr.sort(function (a, b) {
//             return b - a;
//         })

//         for (j = 0; j < mainContents[i].children.length; j++) {
//             mainContents[i].children[j].style.height = `${heightArr[0] * 0.1}rem`
//         };
//         for (j = 0; j < subContents[i].children.length; j++) {
//             subContents[i].children[j].style.height = `${heightArr[0] * 0.1}rem`
//         };
//     };
// }