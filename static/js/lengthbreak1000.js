const length1000 = document.querySelectorAll(".length1000")

for (i = 0; i < length1000.length; i++){
    length1000[i].addEventListener("input", lengthBreak1000)
};

function lengthBreak1000(){
    if(this.value.length > 999){
        alert("최대 입력 글자수를 초과하였습니다.(1000자)")
        this.value = this.value.substr(0, 999);
    }
}