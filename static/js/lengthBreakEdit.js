const editTitle = document.querySelector(".editTitle")
const editTextArea = document.querySelector(".editTextArea")

editTitle.addEventListener("input", lengthBreakTitle)

function lengthBreakTitle(){
    if(this.value.length > 99){
        alert("최대 입력 글자수를 초과하였습니다.(100자)")
        this.value = this.value.substr(0, 99);
    }
}

editTextArea.addEventListener("input", lengthBreakContentes)

function lengthBreakContentes(){
    if(this.value.length > 2999){
        alert("최대 입력 글자수를 초과하였습니다.(3000자)")
        this.value = this.value.substr(0, 2999);
    }
}