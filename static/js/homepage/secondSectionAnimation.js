const title = document.querySelector(".seconedSectionTitle")
const subTitle = document.querySelector(".seconedSectionSubTitle")
const contants = document.querySelector(".seconedSectionContents")

window.addEventListener("scroll", secondAnimation)

function secondAnimation(){
    if(window.scrollY >= 700){
        title.style.opacity = "1"
        title.style.marginRight = "0"
        subTitle.style.opacity = "1"
        subTitle.style.bottom = "0"
        contants.style.opacity = "1"
        contants.style.bottom = "0"
    }
}