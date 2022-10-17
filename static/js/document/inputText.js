const input1 = document.querySelector(".makeText input:nth-child(2)")
const input2 = document.querySelector(".makeText input:nth-child(3)")
const input3 = document.querySelector(".makeText input:nth-child(4)")
const input4 = document.querySelector(".makeText input:nth-child(5)")
const text1 = document.querySelector(".first")
const text2 = document.querySelector(".second")
const text3 = document.querySelector(".third")
const text4 = document.querySelector(".fourth")

window.onload = function () {
        text1.innerText = input1.value
        text2.innerText = input2.value
        text3.innerText = input3.value
        text4.innerText = input4.value
}

input1.addEventListener("input", writing1)
input2.addEventListener("input", writing2)
input3.addEventListener("input", writing3)
input4.addEventListener("input", writing4)

function writing1(){
    text1.innerText = input1.value
}
function writing2(){
    text2.innerText = input2.value
}
function writing3(){
    text3.innerText = input3.value
}
function writing4(){
    text4.innerText = input4.value
}