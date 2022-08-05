const addComma1 = document.querySelectorAll(".tableBody td:nth-child(2)")
const addComma2 = document.querySelectorAll(".tableBody td:nth-child(3)")
const addComma3 = document.querySelectorAll(".tableBody td:nth-child(4)")
const addComma4 = document.querySelectorAll(".tableBody td:nth-child(5)")
const addComma5 = document.querySelectorAll(".tableBody td:nth-child(6)")
const addComma6 = document.querySelectorAll(".tableBody td:nth-child(7)")
const addCommaTotal1 = document.querySelector(".totalTable td:nth-child(2)")
const addCommaTotal2 = document.querySelector(".totalTable td:nth-child(3)")
const addCommaTotal3 = document.querySelector(".totalTable td:nth-child(4)")
const addCommaTotal4 = document.querySelector(".totalTable td:nth-child(5)")
const addCommaTotal5 = document.querySelector(".totalTable td:nth-child(6)")
const addCommaTotal6 = document.querySelector(".totalTable td:nth-child(7)")


// , 추가, 단위추가
window.onload = function () {
    for (i = 0; i < addComma1.length; i++) {
        if (addComma1[i].innerText !== "") {
            addComma1[i].innerText = `${addComma1[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
        if (addComma2[i].innerText !== "") {
            addComma2[i].innerText = `${addComma2[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
        if (addComma3[i].innerText !== "") {
            addComma3[i].innerText = `${addComma3[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
        if (addComma4[i].innerText !== "") {
            addComma4[i].innerText = `${addComma4[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
        if (addComma5[i].innerText !== "") {
            addComma5[i].innerText = `${addComma5[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
        if (addComma6[i].innerText !== "0") {
            addComma6[i].innerText = `${addComma6[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
    }
    if (addCommaTotal1.innerText !== "0") {
        addCommaTotal1.innerText = `${addCommaTotal1.innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
    }
    if (addCommaTotal2.innerText !== "0") {
        addCommaTotal2.innerText = `${addCommaTotal2.innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
    }
    if (addCommaTotal3.innerText !== "0") {
        addCommaTotal3.innerText = `${addCommaTotal3.innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
    }
    if (addCommaTotal4.innerText !== "0") {
        addCommaTotal4.innerText = `${addCommaTotal4.innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
    }
    if (addCommaTotal5.innerText !== "0") {
        addCommaTotal5.innerText = `${addCommaTotal5.innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
    }
    if (addCommaTotal6.innerText !== "0") {
        addCommaTotal6.innerText = `${addCommaTotal6.innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
    }
}