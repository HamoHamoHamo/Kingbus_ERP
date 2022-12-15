const dispatchCheckPopup = document.querySelector(".dispatch_check_popup")
const dispatchCheckHidden = document.querySelector(".dispatch_check_hidden")
const dispatchCheckShowbox = document.querySelectorAll(".dispat_check_showbox")
const dispatchCheckBtn = document.querySelector(".dispatch_check_registration")
const dispatchCheckForm = document.querySelector(".dispatch_check_form")

// 배차확인 팝업 열기
for (i = 0; i < dispatchCheckIcon.length - 1; i++){
    dispatchCheckIcon[i].addEventListener("click", openDispatchCheckPopup)
};

function openDispatchCheckPopup(e){
    e.stopPropagation()

    dispatchCheckShowbox[0].innerText = ""
    dispatchCheckShowbox[1].innerText = ""

    dispatchCheckPopup.style.display = "block"
    
    let thisDate = this.parentNode.parentNode.children[0].children[0].innerText

    if(checkList[thisDate-1] !== ""){
        dispatchCheckShowbox[0].innerText = Object.values(checkList[thisDate-1])[0]
        dispatchCheckShowbox[1].innerText = `${Object.values(checkList[thisDate-1])[1].split(" ")[0]} [${Object.values(checkList[thisDate-1])[1].split(" ")[1]}]`
    }

    if(thisDate <= 9){
        thisDate = `0${thisDate}`
    }
    dispatchCheckHidden.value = `${thisYear}-${thisMonth}-${thisDate}`
}

// 배차확인
dispatchCheckBtn.addEventListener("click", dispatchCheckRegistration)

function dispatchCheckRegistration(){
    if(dispatchCheckShowbox[0].innerText !== ""){
        if(confirm("배차확인을 갱신하시겠습니까?")){
            dispatchCheckForm.submit()
        }else{
            return closePopup(false, "nothing")
        }
    }
    dispatchCheckForm.submit()
}