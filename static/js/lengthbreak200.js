const length200 = document.querySelectorAll(".length200")

for (i = 0; i < length200.length; i++){
    length200[i].addEventListener("input", lengthBreak200)
};

function lengthBreak200(){
    if(this.value.length > 199){
        alert("최대 입력 글자수를 초과하였습니다.(200자)")
        this.value = this.value.substr(0, 199);
    }
}