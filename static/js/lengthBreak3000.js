const length3000 = document.querySelectorAll(".length3000")

for (i = 0; i < length3000.length; i++){
    length3000[i].addEventListener("input", lengthBreak3000)
};

function lengthBreak3000(){
    if(this.value.length > 2999){
        alert("최대 입력 글자수를 초과하였습니다.(3000자)")
        this.value = this.value.substr(0, 2999);
    }
}