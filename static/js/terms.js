const termsCehck = document.querySelectorAll(".checkBox input")
const allCheck = document.querySelector(".allcheck input")



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

function checkingTop(){
  if(allCheck.checked && allCheck[1].checked){

  }
}




// const btn = document.querySelector(".termsButtonNext");
// const checkBoxTop = document.getElementById("agreeToTermsTop");
// const checkBoxBottom = document.getElementById("agreeToTermsBottom");
// const checkBoxAll = document.getElementById("allAgreeTerms");
// const alertTerms = document.querySelectorAll(".alertTerms");



// btn.addEventListener("click", goSignPage);
// checkBoxTop.addEventListener("change", checkingCheckedTop);
// checkBoxBottom.addEventListener("change", checkingCheckedBottom);
// checkBoxAll.addEventListener("change", checkingCheckedAll);

// /*add-alert*/
// function goSignPage(event) {
//   if (checkBoxTop.checked == false) {
//     event.preventDefault();
//     if (checkBoxBottom.checked == false) {
//       alertTerms[0].classList.remove("hidden");
//       alertTerms[1].classList.remove("hidden");
//       alertTerms[0].classList.add("flex");
//       alertTerms[1].classList.add("flex");
//       console.log(alertTerms[0].classList)
//     } else {
//       alertTerms[0].classList.remove("hidden");
//       alertTerms[0].classList.add("flex");
//     }
//   } else if (checkBoxBottom.checked == false) {
//     event.preventDefault();
//     alertTerms[1].classList.remove("hidden");
//     alertTerms[1].classList.add("flex");
//   }
// };

// /*remove-alert*/
// function checkingCheckedTop(){
//   if(checkBoxTop.checked == true){
//     alertTerms[0].classList.remove("flex");
//     alertTerms[0].classList.add("hidden");
//     if(checkBoxBottom.checked == true){
//       checkBoxAll.checked = true;
//     }
//   }else{
//     checkBoxAll.checked = false;
//   }
// }
// function checkingCheckedBottom(){
//   if(checkBoxBottom.checked == true){
//     alertTerms[1].classList.remove("flex");
//     alertTerms[1].classList.add("hidden");
//     if(checkBoxTop.checked == true){
//       checkBoxAll.checked = true;
//     }
//   }else{
//     checkBoxAll.checked = false;
//   }
// }

// /*all-check*/
// function checkingCheckedAll(){
//   if(checkBoxAll.checked == true){
//     checkBoxTop.checked = true;
//     checkBoxBottom.checked = true;
//     alertTerms[0].classList.remove("flex");
//     alertTerms[0].classList.add("hidden");
//     alertTerms[1].classList.remove("flex");
//     alertTerms[1].classList.add("hidden");
//   }else{
//     checkBoxTop.checked = false;
//     checkBoxBottom.checked = false;
//   }
// }