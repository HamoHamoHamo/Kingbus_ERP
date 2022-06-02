const btn = document.querySelector(".getCordnumber");
const cordPage = document.querySelector(".cordnumberInformationBox");
const nextBtn = document.querySelector(".termsButtonNext");

const signInput = document.querySelectorAll(".signupSignupInputCellInput");


btn.addEventListener("click", openCordForm)

function openCordForm(){
  cordPage.classList.remove("hidden");
  cordPage.classList.add("flex");
}

nextBtn.addEventListener("click", validation)

function validation(event){
  event.preventDefault();
  console.log(signInput[0].value);
  if(signInput[0].value == "" || signInput[1].value == "" || signInput[2].value == "" || signInput[3].value == "" || signInput[4].value == "" || signInput[5].value == "" || signInput[6].value == "" || signInput[7].value == "" || signInput[8].value == "" || signInput[9].value == ""){
    event.preventDefault();
  }
}
