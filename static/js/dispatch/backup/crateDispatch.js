const inputBusCount = document.querySelector(".inputBusCount")
const orderDispatch = document.querySelector(".orderDispatch")
const list = document.querySelector(".list")
const inputDispatchForm = document.querySelector(".inputDispatchForm")
const listTableScroll = document.querySelector(".listTableScroll")
const ListTableBox = document.querySelectorAll(".ListTableBox")
const scrollListTableWidth = document.querySelectorAll(".scrollListTableWidth")



inputBusCount.addEventListener("input", test)

function test() {
    if (inputBusCount.value >= 1 && inputBusCount.value < 4) {
        inputDispatchForm.style.height = `${26 + (inputBusCount.value - 1) * 3}rem`
        orderDispatch.style.height = `${6 + (inputBusCount.value - 1) * 3}rem`
        list.style.height = `calc(100% - ${35.2 + (inputBusCount.value - 1) * 3}rem)`
        listTableScroll.style.height = `${39.5 - (inputBusCount.value - 1) * 3}rem`
        ListTableBox[1].style.height = `${36.8 - (inputBusCount.value - 1) * 3}rem`
        scrollListTableWidth[1].style.height = `${39.5 - (inputBusCount.value - 1) * 3}rem`
    }else if(inputBusCount.value >= 4){
        inputDispatchForm.style.height = "33rem"
        orderDispatch.style.height = "13rem"
        list.style.height = "calc(100% - 42.2rem)"
        listTableScroll.style.height = "32.5rem"
        ListTableBox[1].style.height = "30.8rem"
        scrollListTableWidth[1].style.height = "32.5rem"
    }
}