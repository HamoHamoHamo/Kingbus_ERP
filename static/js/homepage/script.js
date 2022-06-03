const mainNav = document.querySelectorAll(".navListLi");
const subNav = document.querySelectorAll(".navListUlSub");
const navBg = document.querySelector(".fullCoverClickBgs");
const mainNavHover = document.querySelectorAll(".navListLiMain");

for (i = 0; i < 3; i++) {
  mainNav[i].addEventListener("click", openNav);
  function openNav() {
    for (i = 0; i < 3; i++) {
      mainNav[i].children[1].classList.remove("visibleFlex");
      mainNav[i].children[0].style.color = "gray";
      this.children[1].classList.add("visibleFlex");
      this.children[0].style.color = "black";
      navBg.classList.add("visibleBlock")
    }
  }
}

navBg.addEventListener("click", closeNav);
function closeNav() {
  for (i = 0; i < 3; i++) {
    mainNav[i].children[1].classList.remove("visibleFlex");
    mainNav[i].children[0].style.color = "gray";
    navBg.classList.remove("visibleBlock")
  }
}

for (i = 0; i < 3; i++) {
  mainNavHover[i].addEventListener("mouseover", navover);
  function navover() {
    this.style.color = "black";
  }
  mainNavHover[i].addEventListener("mouseout", navout);
  function navout() {
    if (this.parentNode.children[1].classList.contains("visibleFlex")) {
      this.style.color = "black";
    }
    else {
      this.style.color = "grey";
    }
  }
}


const hembuger = document.querySelector(".header div img");
const hembugerMenu = document.querySelector(".hembugerMenu");
const hembugerClickMenu = document.querySelectorAll(".hembugerLl");
const hembugerSubUl = document.querySelectorAll(".hembugerSubUl");
const hembugerMenuSide = document.querySelector(".hembugerMenuSide");



hembuger.addEventListener("click", openHembuger);
function openHembuger() {
  if(hembugerMenu.style.display !== "block"){
    hembugerMenu.style.display = "block";
    hembugerMenuSide.style.display = "block";
  }else{
    hembugerMenu.style.display = "none";
    hembugerMenuSide.style.display = "none";
  }
}
hembugerMenuSide.addEventListener("click", closeHembuger);
function closeHembuger(){
  if(hembugerMenuSide.style.display == "block"){
    hembugerMenu.style.display = "none";
    hembugerMenuSide.style.display = "none";
  }
}

for (i = 0; i < 3; i++) {
  hembugerClickMenu[i].addEventListener("click", openSubHembugerMenu);
  function openSubHembugerMenu() {
    for (i = 0; i < 3; i++) {
      hembugerSubUl[i].style.display = "none";
      this.children[1].style.display = "flex";
    }

  }
}
