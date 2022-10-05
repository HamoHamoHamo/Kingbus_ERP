const groupListCellOpenArea = document.querySelectorAll(".groupListCellOpenArea")
const groupoEditeBtn = document.querySelectorAll(".groupoEditeBtn")
const groupDeleteBtn = document.querySelectorAll(".groupDeleteBtn")
const groupSaveBtn = document.querySelectorAll(".groupSaveBtn")
const groupName = document.querySelectorAll(".groupName")
const groupHidden = document.querySelector(".groupHidden")
const groupListForm = document.querySelector(".groupListForm")



// 그룹목록 열고닫기

for (i = 0; i < groupListCellOpenArea.length; i++) {
    groupListCellOpenArea[i].addEventListener("click", openAndClose)
}

function openAndClose() {
    if (this.parentNode.parentNode.children[1].children[0] !== undefined) {
        if (this.classList.contains("openGroup")) {
            this.parentNode.parentNode.childNodes[3].style.height = "0rem"
            const groupArrowIcon = this.parentNode.querySelector(".groupArrowIcon")
            groupArrowIcon.style.transform = "rotate(0deg)"
            this.classList.remove("openGroup")
        } else {
            const routeListCell = this.parentNode.parentNode.querySelectorAll(".routeListCell")
            const groupArrowIcon = this.parentNode.querySelector(".groupArrowIcon")
            for (i = 0; i < routeListCell.length; i++) {
                this.parentNode.parentNode.childNodes[3].style.height = `${(i + 1) * 3}rem`
            }
            groupArrowIcon.style.transform = "rotate(90deg)"
            this.classList.add("openGroup")
        }
    }
}



// 그룹명 & 순번 수정
for (i = 0; i < groupoEditeBtn.length; i++) {
    groupoEditeBtn[i].addEventListener("click", groupTool)
}

function groupTool() {
    for (i = 0; i < groupoEditeBtn.length; i++) {
        groupoEditeBtn[i].parentNode.parentNode.children[1].children[0].style.display = "block"
        groupoEditeBtn[i].parentNode.parentNode.children[1].children[1].style.display = "block"
        groupoEditeBtn[i].parentNode.parentNode.children[1].children[2].style.display = "none"
        groupoEditeBtn[i].parentNode.parentNode.children[0].children[2].readOnly = true
        groupoEditeBtn[i].parentNode.parentNode.children[0].children[2].style.border = "none"
        groupoEditeBtn[i].parentNode.parentNode.children[0].children[2].style.width = "24rem"
        groupoEditeBtn[i].parentNode.parentNode.children[0].children[1].style.display = "none"
        groupoEditeBtn[i].parentNode.parentNode.children[0].children[1].setAttribute("disabled", true)
        groupoEditeBtn[i].parentNode.parentNode.children[0].children[2].setAttribute("disabled", true)
        // groupoEditeBtn[i].parentNode.parentNode.children[0].children[1].disabled = true
        // groupoEditeBtn[i].parentNode.parentNode.children[0].children[2].disabled = true
    }
    this.parentNode.parentNode.children[0].children[1].removeAttribute("disabled")
    this.parentNode.parentNode.children[0].children[2].removeAttribute("disabled")
    this.parentNode.parentNode.children[1].children[0].style.display = "none"
    this.parentNode.parentNode.children[1].children[1].style.display = "none"
    this.parentNode.parentNode.children[1].children[2].style.display = "block"
    this.parentNode.parentNode.children[0].children[2].removeAttribute("readonly")
    this.parentNode.parentNode.children[0].children[2].style.border = "0.1rem solid black"
    this.parentNode.parentNode.children[0].children[2].style.width = "19rem"
    this.parentNode.parentNode.children[0].children[1].style.display = "block"
    groupHidden.value = this.classList[1]
}

for (i = 0; i < groupDeleteBtn.length; i++) {
    groupDeleteBtn[i].addEventListener("click", groupDelete)
}

function groupDelete(e) {
    e.preventDefault()
    groupHidden.value = this.classList[1]
    if (confirm(" 정말로 삭제하시겠습니까?")) {
        groupListForm.action = "/dispatch/regularly/group/delete"
        groupListForm.submit()
    }
}