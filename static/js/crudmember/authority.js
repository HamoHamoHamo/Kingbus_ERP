const alarmArea = document.querySelector(".alarmArea")
function authority(){
    if(AUTHORITY >=4){
        changeFormatBtn.style.display = "none"
        alarmArea.style.display = "none"
    }
}
authority()