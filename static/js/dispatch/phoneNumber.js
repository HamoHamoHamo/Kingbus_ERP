const phoneNmber = document.querySelector("#regularlyOrderCreatePhoneNumber");


phoneNmber.addEventListener("focusout", getPhoneNmberHyphen);
phoneNmber.addEventListener("focusin", removePhoneNmberHyphen);

function getPhoneNmberHyphen() {
  const newString = phoneNmber.value.toString()
    .replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`);
  phoneNmber.value = newString;
  if(phoneNmber.value.length <= 8){
    alert("9자리 이상 입력해 주세요");
    phoneNmber.value = "";
  }
}
function removePhoneNmberHyphen() {
  const newString = phoneNmber.value.toString()
    .replace(/-/g, '')
  phoneNmber.value = newString;
}
