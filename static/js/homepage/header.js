const headerBox = document.querySelector(".headerBox")
const seconedSection = document.querySelector(".seconedSection")
const  menu = document.querySelectorAll(".menuBox li")
const transparentBoxLoge = document.querySelector(".transparentBoxLoge")
const whiteBoxLoge = document.querySelector(".whiteBoxLoge")

window.addEventListener("scroll", whiteHeader)

function whiteHeader(){
    if(window.scrollY > seconedSection.offsetHeight - 60){
        headerBox.classList.add("whiteHeaderBox") 
        for (i = 0; i < menu.length; i++){
            menu[i].classList.remove("menuLi")
            menu[i].classList.add("BlackMenuLi")
        };
        transparentBoxLoge.style.display = "none"
        whiteBoxLoge.style.display = "block"
    }else{
        headerBox.classList.remove("whiteHeaderBox") 
        for (i = 0; i < menu.length; i++){
            menu[i].classList.add("menuLi")
            menu[i].classList.remove("BlackMenuLi")
        };
        transparentBoxLoge.style.display = "block"
        whiteBoxLoge.style.display = "none"
    }
}