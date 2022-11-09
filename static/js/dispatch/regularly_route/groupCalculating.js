const calculate = document.querySelector(".groupCalculateinput input")
const calculateLast = document.querySelector(".groupCalculateinput div")

calculate.addEventListener("input", calculating)

function calculating(){
    if(calculate.value >= 1 && calculate.value <= 27 || calculate.value === ""){
        if(calculate.value == 1 ){
            calculateLast.innerText = "말일"
            calculateLast.parentNode.children[5].innerText = "이번달"
        }else if(calculate.value == ""){
            calculateLast.innerText = ""
            calculateLast.parentNode.children[5].innerText = "다음달"
        }else{
            calculateLast.innerText = `${calculate.value - 1}일`
            calculateLast.parentNode.children[5].innerText = "다음달"
        }
    }else{
        alert("1일에서 27일 까지만 입력이 가능합니다.")
        calculate.value = ""
    }
}