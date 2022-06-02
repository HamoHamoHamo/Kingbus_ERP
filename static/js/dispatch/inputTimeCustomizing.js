const inputTime = document.querySelectorAll(".inputTimeCustomizingForm");
const inputTimeBtn = document.querySelectorAll(".inputTimeCustomizingFormButton");
const inputTimeHours = document.querySelectorAll(".inputTimeCustomizingFormSelectCellHours");
const inputTimeMinute = document.querySelectorAll(".inputTimeCustomizingFormSelectCellMinute");

const inputTimeCustomizing = document.querySelectorAll(".inputTimeCustomizing");
const timeCloseBg = document.querySelector(".timeCloseBg")


for (i = 0; i < 24; i++) {
  inputTimeHours[i].addEventListener("mouseover", mouseoverHours)
  inputTimeHours[i].addEventListener("mouseout", mouseoutHours)
  inputTimeHours[i].addEventListener("click", clickHours)
}
function clickHours() {
  for (i = 0; i < 24; i++) {
    inputTimeHours[i].classList.remove("clickcss");
  }
  this.classList.remove("hovercss");
  this.classList.add("clickcss");
}
function mouseoverHours() {
  if (this.classList.contains("clickcss") == true) {
  } else {
    this.classList.remove("noneActioncss");
    this.classList.add("hovercss");
  }
}
function mouseoutHours() {
  if (this.classList.contains("clickcss") == true) {
  } else {
    this.classList.remove("hovercss");
    this.classList.add("noneActioncss");
  }
}


for (i = 0; i < 60; i++) {
  inputTimeMinute[i].addEventListener("mouseover", mouseoverMinute)
  inputTimeMinute[i].addEventListener("mouseout", mouseoutMinute)
  inputTimeMinute[i].addEventListener("click", clickMinute)
}
function clickMinute() {
  for (i = 0; i < 60; i++) {
    inputTimeMinute[i].classList.remove("clickcss");
  }
  this.classList.remove("hovercss");
  this.classList.add("clickcss");
}
function mouseoverMinute() {
  if (this.classList.contains("clickcss") == true) {
  } else {
    this.classList.remove("noneActioncss");
    this.classList.add("hovercss");
  }
}
function mouseoutMinute() {
  if (this.classList.contains("clickcss") == true) {
  } else {
    this.classList.remove("hovercss");
    this.classList.add("noneActioncss");
  }
}

let targetHours = 0;
let targetMinute = 0;
function findHours() {
  for (i = 0; i < 24; i++) {
    if (inputTimeHours[i].classList.contains("clickcss") == true) {
      targetHours = inputTimeHours[i].innerText;
    }
  }
}
function findMinute() {
  for (i = 0; i < 60; i++) {
    if (inputTimeMinute[i].classList.contains("clickcss") == true) {
      targetMinute = inputTimeMinute[i].innerText;
    }
  }
}


for (i = 24; i < 48; i++) {
  inputTimeHours[i].addEventListener("mouseover", mouseoverHoursBoth)
  inputTimeHours[i].addEventListener("mouseout", mouseoutHoursBoth)
  inputTimeHours[i].addEventListener("click", clickHoursBoth)
}
function clickHoursBoth() {
  for (i = 24; i < 48; i++) {
    inputTimeHours[i].classList.remove("clickcss");
  }
  this.classList.remove("hovercss");
  this.classList.add("clickcss");
}
function mouseoverHoursBoth() {
  if (this.classList.contains("clickcss") == true) {
  } else {
    this.classList.remove("noneActioncss");
    this.classList.add("hovercss");
  }
}
function mouseoutHoursBoth() {
  if (this.classList.contains("clickcss") == true) {
  } else {
    this.classList.remove("hovercss");
    this.classList.add("noneActioncss");
  }
}


for (i = 60; i < 120; i++) {
  inputTimeMinute[i].addEventListener("mouseover", mouseoverMinuteBoth)
  inputTimeMinute[i].addEventListener("mouseout", mouseoutMinuteBoth)
  inputTimeMinute[i].addEventListener("click", clickMinuteBoth)
}
function clickMinuteBoth() {
  for (i = 60; i < 120; i++) {
    inputTimeMinute[i].classList.remove("clickcss");
  }
  this.classList.remove("hovercss");
  this.classList.add("clickcss");
}
function mouseoverMinuteBoth() {
  if (this.classList.contains("clickcss") == true) {
  } else {
    this.classList.remove("noneActioncss");
    this.classList.add("hovercss");
  }
}
function mouseoutMinuteBoth() {
  if (this.classList.contains("clickcss") == true) {
  } else {
    this.classList.remove("hovercss");
    this.classList.add("noneActioncss");
  }
}

let targetHoursBoth = 0;
let targetMinuteBoth = 0;
function findHoursBoth() {
  for (i = 24; i < 48; i++) {
    if (inputTimeHours[i].classList.contains("clickcss") == true) {
      targetHoursBoth = inputTimeHours[i].innerText;
    }
  }
}
function findMinuteBoth() {
  for (i = 60; i < 120; i++) {
    if (inputTimeMinute[i].classList.contains("clickcss") == true) {
      targetMinuteBoth = inputTimeMinute[i].innerText;
    }
  }
}





inputTimeBtn[0].addEventListener("click", clickInputTimeBtn);
function clickInputTimeBtn(event) {
  event.preventDefault();
  inputTime[0].classList.add("nonecss");
  timeCloseBg.classList.add("nonecss");
  findHours();
  findMinute();
  inputTimeCustomizing[0].value = `${targetHours}:${targetMinute}`;

  const afterValue = after.value;
  afterNumver = afterValue.toString()
    .replace(/\:/g, '');
  if(parseInt(afterNumver) > 100){
    sizeComparison();
  }
}

timeCloseBg.addEventListener("click", clicktimeCloseBg);
function clicktimeCloseBg(event) {
  event.preventDefault();
  inputTime[0].classList.add("nonecss");
  timeCloseBg.classList.add("nonecss");
  findHours();
  findMinute();
  inputTimeCustomizing[0].value = `${targetHours}:${targetMinute}`;

  const afterValue = after.value;
  afterNumver = afterValue.toString()
    .replace(/\:/g, '');
  if(parseInt(afterNumver) > 100){
    console.log(parseInt(afterNumver))
    sizeComparison();
  }
}

inputTimeCustomizing[0].addEventListener("click", clickInputTimeCustomizing);
function clickInputTimeCustomizing(){
  inputTime[0].classList.remove("nonecss");
  timeCloseBg.classList.remove("nonecss");

}



inputTimeBtn[1].addEventListener("click", clickInputTimeBtnBoth);
function clickInputTimeBtnBoth(event) {
  event.preventDefault();
  inputTime[1].classList.add("nonecss");
  timeCloseBg.classList.add("nonecss");
  findHoursBoth();
  findMinuteBoth();
  inputTimeCustomizing[1].value = `${targetHoursBoth}:${targetMinuteBoth}`;
  sizeComparison();
}
timeCloseBg.addEventListener("click", clicktimeCloseBgBoth);
function clicktimeCloseBgBoth(event) {
  inputTime[1].classList.add("nonecss");
  timeCloseBg.classList.add("nonecss");
  findHoursBoth();
  findMinuteBoth();
  inputTimeCustomizing[1].value = `${targetHoursBoth}:${targetMinuteBoth}`;
  sizeComparison();
}
inputTimeCustomizing[1].addEventListener("click", clickInputTimeCustomizingBoth);
function clickInputTimeCustomizingBoth(){
  inputTime[1].classList.remove("nonecss");
  timeCloseBg.classList.remove("nonecss");
}