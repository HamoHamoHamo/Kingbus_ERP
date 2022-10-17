const groupList = document.querySelector(".groupList")
const groupCreate = document.querySelector(".groupCreate")
const foldGroup = document.querySelector(".foldGroup")
const groupCloseBtn = document.querySelector(".groupListHead svg")
const groupOpenBtn = document.querySelector(".foldGroup svg")
const groupLayout = document.querySelector(".groupLayout")
const mainLayout = document.querySelector(".mainLayout")


// 그룹 닫기
groupCloseBtn.addEventListener("click", groupClose)

function groupClose(){
    groupList.style.display = "none"
    groupCreate.style.display = "none"
    foldGroup.style.display = "flex"
    groupLayout.style.width = "6rem"
    mainLayout.style.width = "calc(100% - 8rem)"
}



// 그룹 열기
groupOpenBtn.addEventListener("click", groupOpen)

function groupOpen(){
    groupList.style.display = "flex"
    groupCreate.style.display = "flex"
    foldGroup.style.display = "none"
    groupLayout.style.width = "36rem"
    mainLayout.style.width = "calc(100% - 38rem)"
}