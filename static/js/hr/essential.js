const memberEditForm = document.querySelector(".memberEditForm")
const memberEditSaveBtn = document.querySelector(".memberEditSaveBtn")
const editEssential = document.querySelectorAll(".editEssential")
const makeHyphen = document.querySelectorAll(".makeHyphen")

memberEditSaveBtn.addEventListener("click", essentialCheck)

function essentialCheck() {
    for (i = 0; i < editEssential.length; i++) {
        if (editEssential[i].value == "") {
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };

    memberEditForm.submit()
}


for (i = 0; i < makeHyphen.length; i++) {
    makeHyphen[i].addEventListener("input", hyphenMaking)
};



function hyphenMaking() {
    if(this.value.length > 13){
        this.value = this.value.substr(0,13)
    }else{
        this.value = this.value
            .replace(/[^0-9]/g, '')
            .replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`)
    }
}