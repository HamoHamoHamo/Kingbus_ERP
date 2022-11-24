const length100 = document.querySelectorAll(".length100")

for (i = 0; i < length100.length; i++){
    length100[i].addEventListener("input", lengthBreak100)
};

function lengthBreak100(){
    if(this.value.length > 99){
        alert("최대 입력 글자수를 초과하였습니다.(100자)")
        this.value = this.value.substr(0, 99);
    }
}