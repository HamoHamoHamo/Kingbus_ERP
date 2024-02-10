const memberEditForm = document.querySelector(".memberEditForm")
const editEssential = document.querySelectorAll(".editEssential")
const makeHyphen = document.querySelectorAll(".makeHyphen")




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