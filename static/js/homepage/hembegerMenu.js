const hembeger = document.querySelector(".hembeger")
const hembegerMenuBox = document.querySelector(".hembegerMenuBox")
const closeBtnBox = document.querySelector(".closeBtnBox")

hembeger.addEventListener("click", openMenu)

function openMenu(){
    hembegerMenuBox.style.right = "0"
}


closeBtnBox.addEventListener("click", closeMenu)

function closeMenu(){
    hembegerMenuBox.style.right = "-100%"
}