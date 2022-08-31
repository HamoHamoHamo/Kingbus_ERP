const before = document.querySelector("#inputInputBoxInputTwiceBefore");
const after = document.querySelector("#inputInputBoxInputTwiceAfter");
const button = document.querySelectorAll(".inputTimeCustomizingFormButton");
const hours = document.querySelectorAll(".inputTimeCustomizingFormSelectCellHours");
const minute = document.querySelectorAll(".inputTimeCustomizingFormSelectCellMinute");
const ClosedBg = document.querySelector(".timeCloseBg")

// after.addEventListener("focusout", removeString)

// function removeString() {

//   const beforeValue = before.value;
//   beforeNumver = beforeValue.toString()
//     .replace(/\:/g, '');

//   const afterValue = after.value;
//   afterNumver = afterValue.toString()
//     .replace(/\:/g, '');

//   if (parseInt(beforeNumver) >= parseInt(afterNumver)) {
//     alert("시간을 다시 입력해 주세요");
//     after.value = "";
//   }
// }



// const beforeContract = document.querySelector("#inputInputBoxInputTwiceBeforeContract");
// const afterContract = document.querySelector("#inputInputBoxInputTwiceAfterContract");

// afterContract.addEventListener("focusout", removeStringConteract)

// function removeStringConteract() {

//   const beforeContractValue = beforeContract.value;
//   beforeContractNumver = beforeContractValue.toString()
//     .replace(/\-/g, '');

//   const afterContractValue = afterContract.value;
//   afterContractNumver = afterContractValue.toString()
//     .replace(/\-/g, '');

//   if (parseInt(beforeContractNumver) >= parseInt(afterContractNumver)) {
//     alert("기간을 다시 입력해 주세요");
//     afterContract.value = "";
//   }
// }




function sizeComparison() {

  let thisHours = 0;
  let thisMinute = 0;

  const beforeValue = before.value;
  beforeNumver = beforeValue.toString()
    .replace(/\:/g, '');

  for (i = 24; i < 48; i++) {
    if (hours[i].classList.contains("clickcss") == true) {
      thisHours = hours[i].innerText;
    }
  }
  for (i = 60; i < 120; i++) {
    if (minute[i].classList.contains("clickcss") == true) {
      thisMinute = minute[i].innerText;
    }
  }
  let afterValue = `${thisHours}${thisMinute}`;

  if (parseInt(beforeNumver) >= parseInt(afterValue)) {
    alert("시간을 다시 입력해 주세요");
    inputTimeCustomizing[1].value = "";
  }
}