const sideNavControll = document.querySelectorAll(".nav1BoxMenuHaveDepth2 svg")
const nav1BoxMenuHaveDepth2 = document.querySelectorAll(".nav1BoxMenuHaveDepth2")
const sideMenuNav2Box = document.querySelectorAll(".sideMenuNav2Box")
const sideMenuNav2 = document.querySelectorAll(".sideMenuNav2")
const nav1Box = document.querySelectorAll(".nav1Box")

let overlapCount = 111;
let navOpenCount = false;

for (i = 0; i < nav1BoxMenuHaveDepth2.length; i++) {
  nav1BoxMenuHaveDepth2[i].addEventListener("click", openSideNav)
}

function openSideNav() {
  for (i = 0; i < nav1BoxMenuHaveDepth2.length; i++) {
    sideMenuNav2Box[i].style.height = "0";
    sideMenuNav2[i].style.height = "0"
    sideNavControll[i].style.transform = "rotate(0deg)"
    nav1Box[i+1].style.backgroundColor = "#1C1A4E";
  }
  if (overlapCount == Array.from(nav1BoxMenuHaveDepth2).indexOf(this)) {
    sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "0";
    sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "0"
    overlapCount = 111;
    navOpenCount = false;
  } else {
    switch (Array.from(nav1BoxMenuHaveDepth2).indexOf(this)) {
      case 0:
        sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "10.4rem";
        sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "8.4rem";
        break;
      case 1:
        sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "15.2rem";
        sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "13.2rem";
        break;
      case 2:
        sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "5.6rem";
        sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "3.6rem";
        break;
      case 3:
        sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "20rem";
        sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "18rem";
        break;
      case 4:
        sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "15.2rem";
        sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "13.2rem";
        break;
      case 5:
        sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "10.4rem";
        sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "8.4rem";
        break;
    }
    sideNavControll[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.transform = "rotate(180deg)"
    nav1Box[parseInt(`${Array.from(nav1BoxMenuHaveDepth2).indexOf(this)}`) + 1].style.backgroundColor = "#19173B";
    overlapCount = Array.from(nav1BoxMenuHaveDepth2).indexOf(this);
    navOpenCount = true;
  }
}


//hover 색 변화
for (i = 0; i < nav1Box.length; i++) {
  nav1Box[i].addEventListener('mouseover', bgThis)
  nav1Box[i].addEventListener('mouseout', bgNotThis)
}

function bgThis() {
  if (!navOpenCount) {
    this.style.backgroundColor = "#19173B"
  }
}

function bgNotThis() {
  if (!navOpenCount) {
    this.style.backgroundColor = "#1C1A4E"
  }
}