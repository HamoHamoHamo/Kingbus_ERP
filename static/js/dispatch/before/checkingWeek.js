const checkboxWeek = document.querySelectorAll(".inputInputBoxCheckboxDateCheckbox")

checkboxWeek[0].addEventListener("click", checkingAllDay)
checkboxWeek[1].addEventListener("click", checkingMonlDay)
checkboxWeek[2].addEventListener("click", checkingTuelDay)
checkboxWeek[3].addEventListener("click", checkingWedlDay)
checkboxWeek[4].addEventListener("click", checkingThulDay)
checkboxWeek[5].addEventListener("click", checkingFrilDay)
checkboxWeek[6].addEventListener("click", checkingSatlDay)
checkboxWeek[7].addEventListener("click", checkingSunlDay)


function checkingAllDay() {
  if (checkboxWeek[0].checked == true) {
    for (i = 1; 1 < 8; i++) {
      checkboxWeek[i].checked = true;
    }
  } else {
    for (i = 1; 1 < 8; i++) {
      checkboxWeek[i].checked = false;
    }
  }
}

function checkingMonlDay() {
  if (checkboxWeek[1].checked == false) {
    checkboxWeek[0].checked = false;
  }else{
    if(checkboxWeek[2].checked == true && checkboxWeek[3].checked == true && checkboxWeek[4].checked == true && checkboxWeek[5].checked == true && checkboxWeek[6].checked == true && checkboxWeek[7].checked == true){
      checkboxWeek[0].checked = true;
    }
  }
}
function checkingTuelDay() {
  if (checkboxWeek[2].checked == false) {
    checkboxWeek[0].checked = false;
  }else{
    if(checkboxWeek[1].checked == true && checkboxWeek[3].checked == true && checkboxWeek[4].checked == true && checkboxWeek[5].checked == true && checkboxWeek[6].checked == true && checkboxWeek[7].checked == true){
      checkboxWeek[0].checked = true;
    }
  }
}
function checkingWedlDay() {
  if (checkboxWeek[3].checked == false) {
    checkboxWeek[0].checked = false;
  }else{
    if(checkboxWeek[2].checked == true && checkboxWeek[1].checked == true && checkboxWeek[4].checked == true && checkboxWeek[5].checked == true && checkboxWeek[6].checked == true && checkboxWeek[7].checked == true){
      checkboxWeek[0].checked = true;
    }
  }
}
function checkingThulDay() {
  if (checkboxWeek[4].checked == false) {
    checkboxWeek[0].checked = false;
  }else{
    if(checkboxWeek[2].checked == true && checkboxWeek[3].checked == true && checkboxWeek[1].checked == true && checkboxWeek[5].checked == true && checkboxWeek[6].checked == true && checkboxWeek[7].checked == true){
      checkboxWeek[0].checked = true;
    }
  }
}
function checkingFrilDay() {
  if (checkboxWeek[5].checked == false) {
    checkboxWeek[0].checked = false;
  }else{
    if(checkboxWeek[2].checked == true && checkboxWeek[3].checked == true && checkboxWeek[4].checked == true && checkboxWeek[1].checked == true && checkboxWeek[6].checked == true && checkboxWeek[7].checked == true){
      checkboxWeek[0].checked = true;
    }
  }
}
function checkingSatlDay() {
  if (checkboxWeek[6].checked == false) {
    checkboxWeek[0].checked = false;
  }else{
    if(checkboxWeek[2].checked == true && checkboxWeek[3].checked == true && checkboxWeek[4].checked == true && checkboxWeek[5].checked == true && checkboxWeek[1].checked == true && checkboxWeek[7].checked == true){
      checkboxWeek[0].checked = true;
    }
  }
}
function checkingSunlDay() {
  if (checkboxWeek[7].checked == false) {
    checkboxWeek[0].checked = false;
  }else{
    if(checkboxWeek[2].checked == true && checkboxWeek[3].checked == true && checkboxWeek[4].checked == true && checkboxWeek[5].checked == true && checkboxWeek[6].checked == true && checkboxWeek[1].checked == true){
      checkboxWeek[0].checked = true;
    }
  }
}


