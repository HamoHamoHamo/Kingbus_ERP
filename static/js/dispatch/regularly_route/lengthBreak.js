const length15 = document.querySelectorAll(".length15")

for (i = 0; i < length15.length; i++){
    length15[i].addEventListener("input", lengthBreak15)
};

function lengthBreak15(){
    if(this.value.length > 15){
        alert("최대 입력 글자수를 초과하였습니다.(15자)")
        this.value = this.value.substr(0, 15);
    }
}


const length50 = document.querySelectorAll(".length50")

for (i = 0; i < length50.length; i++){
    length50[i].addEventListener("input", lengthBreak50)
};

function lengthBreak50(){
    if(this.value.length > 50){
        alert("최대 입력 글자수를 초과하였습니다.(50자)")
        this.value = this.value.substr(0, 50);
    }
}