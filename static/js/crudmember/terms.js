const termsCehck = document.querySelectorAll(".checkBox input")
const allCheck = document.querySelector(".allcheck input")
const nextStepBtn = document.querySelector(".nextStepBtn")



//allcheck 
allCheck.addEventListener("change", allChecking)

function allChecking() {
  if (allCheck.checked) {
    for (i = 0; i < 2; i++) {
      termsCehck[i].checked = true
    }
  } else {
    for (i = 0; i < 2; i++) {
      termsCehck[i].checked = false
    }
  }
}



// checkedTop
termsCehck[0].addEventListener("change", checkingTop)

function checkingTop() {
  if (!allCheck.checked && termsCehck[1].checked) {
    allCheck.checked = true
  } else if (allCheck.checked && termsCehck[1].checked) {
    allCheck.checked = false
  }
}



// checkedBottom
termsCehck[1].addEventListener("change", checkingBottom)

function checkingBottom() {
  if (!allCheck.checked && termsCehck[0].checked) {
    allCheck.checked = true
    console.log("A")
  } else if (allCheck.checked && termsCehck[0].checked) {
    allCheck.checked = false
  }
}




//allcheck 
nextStepBtn.addEventListener("click", nextBtn)

function nextBtn(event) {
  if (!allCheck.checked) {
    event.preventDefault();
    alert("약관에 모두 동의해 주세요.")
  }
}