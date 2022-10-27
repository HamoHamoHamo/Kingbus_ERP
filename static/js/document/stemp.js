const addStemp = document.querySelector(".addStemp")
const stemp = document.querySelectorAll(".stemp")

addStemp.addEventListener("click", visibleStemp)

function visibleStemp(){
    if(addStemp.innerText == "도장빼기"){
        addStemp.innerText = "도장넣기"
        addStemp.style.backgrounColor = "#444"
        for (i = 0; i < stemp.length; i++){
            stemp[i].style.display = "none"
        };
    }else{
        addStemp.innerText = "도장빼기"
        addStemp.style.backgrounColor = "rgb(155, 151, 151)"
        for (i = 0; i < stemp.length; i++){
            stemp[i].style.display = "block"
        };
    }
}