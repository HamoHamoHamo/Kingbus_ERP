const thirdSection = document.querySelector(".thirdSection")
const thirdSectionBg2 = document.querySelector(".thirdSectionBg2")
const thirdSectionBg3 = document.querySelector(".thirdSectionBg3")
const thirdSectionBg4 = document.querySelector(".thirdSectionBg4")
const thirdSectionBg5 = document.querySelector(".thirdSectionBg5")
const thirdSectionBg6 = document.querySelector(".thirdSectionBg6")


const thirdMainTitle = document.querySelector(".thirdMainTitle")

const visibleFirst = document.querySelector(".visibleFirst")
const visibleFirstTitle = document.querySelector(".visibleFirst span:nth-child(1)")
const visibleFirstSubTitle = document.querySelector(".visibleFirst span:nth-child(2)")
const visibleFirstIcon = document.querySelector(".visibleFirst img")

const visibleSecond = document.querySelector(".visibleSecond")
const visibleSecondTitle = document.querySelector(".visibleSecondTitle")
const visibleSecondContents = document.querySelector(".visibleSecondContents")

const visibleThird = document.querySelector(".visibleThird")
const visibleThirdTitle = document.querySelector(".visibleThirdTitle")
const visibleThirdContents = document.querySelector(".visibleThirdContents")

const visibleFourth = document.querySelector(".visibleFourth")
const visibleFourthTitle = document.querySelector(".visibleFourthTitle")
const visibleFourthContents = document.querySelector(".visibleFourthContents")

const visibleFifth = document.querySelector(".visibleFifth")
const visibleFifthTitle = document.querySelector(".visibleFifthTitle")
const visibleFifthContents = document.querySelector(".visibleFifthContents")

const visibleSixth = document.querySelector(".visibleSixth")
const visibleSixthTitle = document.querySelector(".visibleSixthTitle")
const visibleSixthContents = document.querySelector(".visibleSixthContents")



window.addEventListener("wheel", function (e) {
    e.preventDefault();
}, { passive: false });

window.addEventListener("wheel", thirdAnimation)

let scrolling = 0
let thirdBg = 0
let eventContinue = true

function thirdAnimation(e) {
    if (eventContinue) {
        setTimeout(function () {
            eventContinue = false
            if (e.deltaY > 0 && scrolling <= 3) {
                if (scrolling == 1) {
                    scrolling = scrolling + 1
                    window.scrollTo({ left: 0, top: scrolling * window.innerHeight, behavior: "smooth" });
                    thirdAnimationFirst()
                } else if (scrolling == 2) {
                    if(thirdBg <= 4){
                        thirdBg = thirdBg + 1
                        BgUp()
                    }else{
                        scrolling = scrolling + 1
                        window.scrollTo({ left: 0, top: scrolling * window.innerHeight, behavior: "smooth" });
                    }
                }else if(scrolling == 3){
                    scrolling = scrolling + 1
                    window.scrollTo({ left: 0, top: (scrolling - 1) * window.innerHeight + 64, behavior: "smooth" });
                }else {
                    scrolling = scrolling + 1
                    window.scrollTo({ left: 0, top: scrolling * window.innerHeight, behavior: "smooth" });
                }
            } else if (e.deltaY < 0 && scrolling >= 0) {
                if (scrolling == 2) {
                    if (thirdBg == 0) {
                        scrolling = scrolling - 1
                        window.scrollTo({ left: 0, top: scrolling * window.innerHeight, behavior: "smooth" });
                    } else {
                        BgDown()
                    }
                    thirdBg = thirdBg - 1
                } else {
                    scrolling = scrolling - 1
                    window.scrollTo({ left: 0, top: scrolling * window.innerHeight, behavior: "smooth" });
                }
            }
            setTimeout(() => eventContinue = true, 600)
        }, 0)
    }
}

function BgUp() {
    if (thirdBg == 1) {
        thirdSectionBg2.style.top = "0%"
        thirdAnimationSecond()
    } else if (thirdBg == 2) {
        thirdAnimationThird()
        thirdSectionBg3.style.top = "0%"
    } else if (thirdBg == 3) {
        thirdAnimationFourth()
        thirdSectionBg4.style.top = "0%"
    } else if (thirdBg == 4) {
        thirdAnimationFifth()
        thirdSectionBg5.style.top = "0%"
    } else if (thirdBg == 5) {
        thirdAnimationSixth()
        thirdSectionBg6.style.top = "0%"
    }
}

function BgDown() {
    if (thirdBg == 1) {
        returnSecond()
        thirdSectionBg2.style.top = "108%"
    } else if (thirdBg == 2) {
        returnThird()
        thirdSectionBg3.style.top = "108%"
    } else if (thirdBg == 3) {
        returnFourth()
        thirdSectionBg4.style.top = "108%"
    } else if (thirdBg == 4) {
        returnFifth()
        thirdSectionBg5.style.top = "108%"
    } else if (thirdBg == 5) {
        returnSixth()
        thirdSectionBg6.style.top = "108%"
    }
}

function thirdAnimationFirst() {
    thirdMainTitle.style.width = "100rem"
    visibleFirstTitle.style.top = "10%"
    visibleFirstTitle.style.opacity = "1"
    visibleFirstSubTitle.style.top = "30%"
    visibleFirstSubTitle.style.opacity = "1"
    visibleFirstIcon.style.top = "56%"
    visibleFirstIcon.style.opacity = "1"
}

function thirdAnimationSecond() {
    visibleFirst.style.opacity = "0"
    thirdMainTitle.style.height = "28rem"
    setTimeout(function () {
        thirdMainTitle.style.transitionDelay = "1.4s"
        setTimeout(function () {
            visibleFirst.style.display = "none"
            visibleSecond.style.display = "flex"
            thirdMainTitle.style.top = "60%"
            thirdMainTitle.style.left = "50rem"
            setTimeout(function () {
                visibleSecondTitle.style.top = "20%"
                visibleSecondTitle.style.opacity = "1"
                visibleSecondContents.style.top = "60%"
                visibleSecondContents.style.opacity = "1"
            }, 800)
        }, 0)
    }, 0)
}

function returnSecond() {
    setTimeout(function(){
        visibleSecond.style.display = "none"
        thirdMainTitle.style.transitionDelay = "0.6s"
        visibleSecondTitle.style.top = "16%"
        visibleSecondTitle.style.opacity = "0"
        visibleSecondContents.style.top = "56%"
        visibleSecondContents.style.opacity = "0"
        setTimeout(function(){
            thirdMainTitle.style.top = "50%"
            thirdMainTitle.style.left = "50%"
            setTimeout(function(){
                thirdMainTitle.style.height = "42rem"
                setTimeout(function(){
                    visibleFirst.style.opacity = "1"
                    visibleFirst.style.display = "flex"
                },1400)
            },600)
        },0)
    },200)
}


function thirdAnimationThird() {
    visibleSecond.style.display = "none"
    visibleThird.style.display = "flex"
    setTimeout(function () {
        visibleThirdTitle.style.top = "20%"
        visibleThirdTitle.style.opacity = "1"
        visibleThirdContents.style.top = "60%"
        visibleThirdContents.style.opacity = "1"
    }, 100)
}

function returnThird() {
    setTimeout(function(){
        visibleSecond.style.display = "flex"
        visibleThird.style.display = "none"
        visibleThirdTitle.style.top = "16%"
        visibleThirdTitle.style.opacity = "0"
        visibleThirdContents.style.top = "56%"
        visibleThirdContents.style.opacity = "0"
    },200)
}

function thirdAnimationFourth() {
    visibleThird.style.display = "none"
    visibleFourth.style.display = "flex"
    setTimeout(function () {
        visibleFourthTitle.style.top = "20%"
        visibleFourthTitle.style.opacity = "1"
        visibleFourthContents.style.top = "60%"
        visibleFourthContents.style.opacity = "1"
    }, 100)
}

function returnFourth() {
    setTimeout(function(){
        visibleThird.style.display = "flex"
        visibleFourth.style.display = "none"
        visibleFourthTitle.style.top = "16%"
        visibleFourthTitle.style.opacity = "0"
        visibleFourthContents.style.top = "56%"
        visibleFourthContents.style.opacity = "0"
    },200)
}

function thirdAnimationFifth() {
    visibleFourth.style.display = "none"
    visibleFifth.style.display = "flex"
    setTimeout(function () {
        visibleFifthTitle.style.top = "20%"
        visibleFifthTitle.style.opacity = "1"
        visibleFifthContents.style.top = "60%"
        visibleFifthContents.style.opacity = "1"
    }, 100)
}

function returnFifth() {
    setTimeout(function(){
        visibleFourth.style.display = "flex"
        visibleFifth.style.display = "none"
        visibleFifthTitle.style.top = "16%"
        visibleFifthTitle.style.opacity = "0"
        visibleFifthContents.style.top = "56%"
        visibleFifthContents.style.opacity = "0"
    },200)
}

function thirdAnimationSixth() {
    visibleFifth.style.display = "none"
    visibleSixth.style.display = "flex"
    setTimeout(function () {
        visibleSixthTitle.style.top = "20%"
        visibleSixthTitle.style.opacity = "1"
        visibleSixthContents.style.top = "60%"
        visibleSixthContents.style.opacity = "1"
    }, 100)
}

function returnSixth() {
    setTimeout(function(){
        visibleFifth.style.display = "flex"
        visibleSixth.style.display = "none"
        visibleSixthTitle.style.top = "16%"
        visibleSixthTitle.style.opacity = "0"
        visibleSixthContents.style.top = "56%"
        visibleSixthContents.style.opacity = "0"
    },200)
}