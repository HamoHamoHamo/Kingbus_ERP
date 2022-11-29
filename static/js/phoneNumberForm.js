const phoneNumber = document.querySelectorAll(".phoneNumber")

for (i = 0; i < phoneNumber.length; i++){
    phoneNumber[i].addEventListener("input", phoneNumberForm)
};
function phoneNumberForm(){
    this.value = this.value
   .replace(/[^0-9]/g, '')
  .replace(/^(\d{0,3})(\d{0,4})(\d{0,4})$/g, "$1-$2-$3").replace(/(\-{1,2})$/g, "");
}