const addStemp = document.querySelector(".addStemp")
const stemp = document.querySelector(".stemp")

addStemp.addEventListener("click", visibleStemp)

function visibleStemp(){
    if(addStemp.innerText == "도장빼기"){
        addStemp.innerText = "도장넣기"
        addStemp.style.backgrounColor = "#444"
        stemp.style.display = "none"
    }else{
        addStemp.innerText = "도장빼기"
        addStemp.style.backgrounColor = "rgb(155, 151, 151)"
        stemp.style.display = "block"
    }
}