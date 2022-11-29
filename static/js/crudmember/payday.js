const dayValidation = document.querySelector(".dayValidation")

dayValidation.addEventListener("input", Low27)
dayValidation.addEventListener("change", over27)

function Low27(){
    this.value = this.value.replace(/[^0-9]/g,'');
    if(this.value > 31){
        this.value = ""
    }
}

function over27(){
    if(this.value > 27 && this.value <= 31){
        this.value = "말일"
    }
}