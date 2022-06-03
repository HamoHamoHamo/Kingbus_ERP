const sideNavControll = document.querySelectorAll(".nav1BoxMenu img:nth-last-child(1)")
const nav1BoxMenuHaveDepth2 = document.querySelectorAll(".nav1BoxMenuHaveDepth2")
const sideMenuNav2Box = document.querySelectorAll(".sideMenuNav2Box")
const sideMenuNav2 = document.querySelectorAll(".sideMenuNav2")
const nav1Box = document.querySelectorAll(".nav1Box")

let overlapCount = 111;

for (i = 0; i < 5; i++) {
  nav1BoxMenuHaveDepth2[i].addEventListener("click", openSideNav)
}

function openSideNav() {
  for (i = 0; i < 5; i++) {
    sideMenuNav2Box[i].style.height = "0";
    sideMenuNav2[i].style.height = "0"
    sideNavControll[i].style.transform = "rotate(0deg)"
    nav1Box[i].style.backgroundColor = "transparent";
  }
  if (overlapCount == Array.from(nav1BoxMenuHaveDepth2).indexOf(this)) {
    sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "0";
    sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "0"
    overlapCount = 111;
  } else {
    switch (Array.from(nav1BoxMenuHaveDepth2).indexOf(this)) {
      case 0:
        sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "10.4rem";
        sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "8.4rem";
        break;
      case 1:
        sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "23rem";
        sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "21rem";
        break;
      case 2:
        sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "10.4rem";
        sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "8.4rem";
        break;
      case 3:
        sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "15.2rem";
        sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "13.2rem";
        break;
      case 4:
        sideMenuNav2Box[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "10.4rem";
        sideMenuNav2[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.height = "8.4rem";
        break;
    }
    sideNavControll[Array.from(nav1BoxMenuHaveDepth2).indexOf(this)].style.transform = "rotate(180deg)"
    nav1Box[parseInt(`${Array.from(nav1BoxMenuHaveDepth2).indexOf(this)}`)+1].style.backgroundColor = "#19173B";
    overlapCount = Array.from(nav1BoxMenuHaveDepth2).indexOf(this);
  }
}