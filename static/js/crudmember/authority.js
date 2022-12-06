const alarmArea = document.querySelector(".alarmArea")
function authority(){
    if(AUTHORITY >=3){
        changeFormatBtn.style.display = "none"
        alarmArea.style.display = "none"
    }
}
authority()