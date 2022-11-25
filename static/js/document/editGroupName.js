const groupNameEditBtn = document.querySelectorAll(".groupNameEditBtn")
const groupName = document.querySelectorAll(".groupName")
const groupNameSaveBtn = document.querySelectorAll(".groupNameSaveBtn")
const groupNameDeleteBtn = document.querySelectorAll(".groupNameDeleteBtn")
const GroupIdHidden = document.querySelector(".hiddenGroupId")


// 그룹이름 수정
for (i = 0; i < groupNameEditBtn.length; i++) {
    groupNameEditBtn[i].addEventListener("click", editgroupName)
}

function editgroupName(e) {
    this.style.display = "none"
    this.parentNode.children[3].style.display = "flex"
    this.parentNode.children[1].children[0].classList.add("editGroupName")
    this.parentNode.children[1].children[0].disabled = false;
    e.stopPropagation()
}


// 그룹이름 버블링 방지
for (i = 0; i < groupName.length; i++) {
    groupName[i].addEventListener("click", blockbubbleing)
}

function blockbubbleing(e) {
    e.stopPropagation()
}


// 그룹이름 저장 url변경
for (i = 0; i < groupNameSaveBtn.length; i++) {
    groupNameSaveBtn[i].addEventListener("click", saveGroupName)
}

function saveGroupName(e) {
    e.stopPropagation()
    if(this.parentNode.children[1].children[0].value == ""){
        return alert("입력하지 않은 필수 입력사항이 있습니다.")
    }
    GroupIdHidden.value = `${this.parentNode.parentNode.parentNode.children[0].children[0].value}`
    contentsAreaBox.action = "company/group/edit"
    contentsAreaBox.submit()
}


// 그룹이름 삭제 url변경
for (i = 0; i < groupNameDeleteBtn.length; i++) {
    groupNameDeleteBtn[i].addEventListener("click", deleteFolderUrl)
}

function deleteFolderUrl(e) {
    e.stopPropagation()
    if(confirm("정말로 삭제하시겠습니까?")){
        GroupIdHidden.value = `${this.parentNode.parentNode.parentNode.children[0].children[0].value}`
        contentsAreaBox.action = "company/group/delete"
        contentsAreaBox.submit()
    }else{
        return;   
    }
    
}