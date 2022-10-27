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
const visibleFirstIcon = document.querySelector(".visibleFirst img:nth-child(3)")
const visibleFirstIconSmall = document.querySelector(".visibleFirst img:nth-child(4)")

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

const body = document.querySelector("body")

window.onload = function size() {
    if (window.innerWidth < 768) {
        body.style.height  = "100%"
        body.style.overflow = "hidden"
        body.style.touchAction  = "none"
    }
    console.log();
}

window.addEventListener("wheel", function (e) {
    e.preventDefault();
}, { passive: false });


window.addEventListener("wheel", thirdAnimation)

window.addEventListener("touchstart", mobileTouchStart)
window.addEventListener("touchend", mobileTouchEnd)

let startPoint = ""
function mobileTouchStart(event) {
    startPoint = event.changedTouches[0].clientY
}

let endPoint = ""
function mobileTouchEnd(event) {
    endPoint = event.changedTouches[0].clientY
    mobileFunction()
}

let scrolling = 0
let thirdBg = 0
let eventContinue = true




function mobileFunction() {
    let upScroll = false
    let downScroll = false
    if (startPoint - endPoint > 10) {
        upScroll = true
    } else if(startPoint - endPoint < -10){
        downScroll = true
    }
    if (eventContinue) {
        setTimeout(function () {
            eventContinue = false
            if (upScroll && scrolling <= 3) {
                if (scrolling == 1) {
                    scrolling = scrolling + 1
                    scrollingAnimation(scrolling)
                    thirdAnimationFirst()
                } else if (scrolling == 2) {
                    if (thirdBg <= 4) {
                        thirdBg = thirdBg + 1
                        BgUp()
                    } else {
                        scrolling = scrolling + 1
                        scrollingAnimation(scrolling)
                    }
                } else if (scrolling == 3) {
                    scrolling = scrolling + 1
                    scrollingAnimation(scrolling)
                } else {
                    scrolling = scrolling + 1
                    scrollingAnimation(scrolling)
                }
            } else if (downScroll && scrolling >= 0) {
                if (scrolling == 2) {
                    if (thirdBg <= 0) {
                        thirdBg = 0
                        scrolling = scrolling - 1
                        scrollingAnimation(scrolling)
                    } else {
                        BgDown()
                        thirdBg = thirdBg - 1
                    }
                } else {
                    scrolling = scrolling - 1
                    scrollingAnimation(scrolling)
                }
            }
            setTimeout(() => eventContinue = true, 600)
        }, 0)
    }
}

function thirdAnimation(e) {
    if (window.innerWidth >= 768) {
        if (eventContinue) {
            setTimeout(function () {
                eventContinue = false
                if (e.deltaY > 0 && scrolling <= 3) {
                    if (scrolling == 1) {
                        scrolling = scrolling + 1
                        scrollingAnimation(scrolling)
                        thirdAnimationFirst()
                    } else if (scrolling == 2) {
                        if (thirdBg <= 4) {
                            thirdBg = thirdBg + 1
                            BgUp()
                        } else {
                            scrolling = scrolling + 1
                            scrollingAnimation(scrolling)
                        }
                    } else if (scrolling == 3) {
                        scrolling = scrolling + 1
                        scrollingAnimation(scrolling)
                    } else {
                        scrolling = scrolling + 1
                        scrollingAnimation(scrolling)
                    }
                } else if (e.deltaY < 0 && scrolling >= 0) {
                    if (scrolling == 2) {
                        if (thirdBg <= 0) {
                            thirdBg = 0
                            scrolling = scrolling - 1
                            scrollingAnimation(scrolling)
                        } else {
                            BgDown()
                            thirdBg = thirdBg - 1
                        }
                    } else {
                        scrolling = scrolling - 1
                        scrollingAnimation(scrolling)
                    }
                }
                setTimeout(() => eventContinue = true, 600)
            }, 0)
        }
    }
}


function scrollingAnimation(scrolling) {
    window.scrollTo({ left: 0, top: scrolling * document.documentElement.clientHeight, behavior: "smooth" });
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
    if (window.innerWidth > 1560) {
        thirdMainTitle.style.width = "100rem"
    } else if (window.innerWidth <= 1560 && window.innerWidth >= 1024) {
        thirdMainTitle.style.width = "80rem"
    } else if (window.innerWidth < 1024) {
        thirdMainTitle.style.width = "80%"
    } else if (window.innerWidth < 440) {
        thirdMainTitle.style.width = "92%"
    }
    visibleFirstTitle.style.top = "10%"
    visibleFirstTitle.style.opacity = "1"
    visibleFirstSubTitle.style.opacity = "1"
    if (window.innerWidth >= 768) {
        visibleFirstIcon.style.top = "56%"
        visibleFirstSubTitle.style.top = "30%"
        visibleFirstIcon.style.opacity = "1"
    } else if (window.innerWidth < 768) {
        visibleFirstSubTitle.style.top = "26%"
        visibleFirstIconSmall.style.top = "50%"
        visibleFirstIconSmall.style.opacity = "1"
    }
}

function thirdAnimationSecond() {
    visibleFirst.style.opacity = "0"

    if (window.innerWidth > 1560) {
        thirdMainTitle.style.height = "28rem"
    } else if (window.innerWidth <= 1560 && window.innerWidth >= 1024) {
        thirdMainTitle.style.height = "26rem"
    } else if (window.innerWidth < 1024 && window.innerWidth >= 768) {
        thirdMainTitle.style.height = "26rem"
    } else if (window.innerWidth < 768 && window.innerWidth >= 560) {
        thirdMainTitle.style.height = "24rem"
    } else if (window.innerWidth < 560 && window.innerWidth >= 440) {
        thirdMainTitle.style.height = "20rem"
    }
    setTimeout(function () {
        thirdMainTitle.style.transitionDelay = "1.4s"
        setTimeout(function () {
            visibleFirst.style.display = "none"
            visibleSecond.style.display = "flex"

            if (window.innerWidth >= 1024) {
                thirdMainTitle.style.top = "60%"
            } else if (window.innerWidth < 1024 && window.innerWidth >= 768) {
                thirdMainTitle.style.top = "50%"
            }

            console.log(window.innerWidth);
            if (window.innerWidth > 1560) {
                thirdMainTitle.style.left = "50rem"
            } else if (window.innerWidth <= 1560 && window.innerWidth >= 1024) {
                thirdMainTitle.style.left = "40rem"
            } else if (window.innerWidth < 1024 && window.innerWidth >= 768) {
                thirdMainTitle.style.left = "50%"
            }
            setTimeout(function () {
                visibleSecondTitle.style.top = "20%"
                visibleSecondTitle.style.opacity = "1"
                if (window.innerWidth >= 768) {
                } else if (window.innerWidth < 768 && window.innerWidth >= 560) {
                    visibleSecondContents.style.top = "68%"
                } else if (window.innerWidth < 560 && window.innerWidth >= 440) {
                    visibleSecondContents.style.top = "64%"
                }
                visibleSecondContents.style.opacity = "1"
            }, 800)
        }, 0)
    }, 0)
}

function returnSecond() {
    setTimeout(function () {
        visibleSecond.style.display = "none"
        thirdMainTitle.style.transitionDelay = "0.6s"
        visibleSecondTitle.style.top = "16%"
        visibleSecondTitle.style.opacity = "0"
        visibleSecondContents.style.top = "56%"
        visibleSecondContents.style.opacity = "0"
        setTimeout(function () {
            thirdMainTitle.style.top = "50%"
            thirdMainTitle.style.left = "50%"
            setTimeout(function () {
                if (window.innerWidth >= 1024) {
                    thirdMainTitle.style.height = "42rem"
                } else if (window.innerWidth < 1024 && window.innerWidth >= 768) {
                    thirdMainTitle.style.height = "36rem"
                } else if (window.innerWidth < 768 && window.innerWidth >= 560) {
                    thirdMainTitle.style.height = "40rem"
                } else if (window.innerWidth < 560 && window.innerWidth >= 440) {
                    thirdMainTitle.style.height = "30rem"
                }
                setTimeout(function () {
                    visibleFirst.style.opacity = "1"
                    visibleFirst.style.display = "flex"
                }, 1400)
            }, 600)
        }, 0)
    }, 200)
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
    setTimeout(function () {
        visibleSecond.style.display = "flex"
        visibleThird.style.display = "none"
        visibleThirdTitle.style.top = "16%"
        visibleThirdTitle.style.opacity = "0"
        visibleThirdContents.style.top = "56%"
        visibleThirdContents.style.opacity = "0"
    }, 200)
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
    setTimeout(function () {
        visibleThird.style.display = "flex"
        visibleFourth.style.display = "none"
        visibleFourthTitle.style.top = "16%"
        visibleFourthTitle.style.opacity = "0"
        visibleFourthContents.style.top = "56%"
        visibleFourthContents.style.opacity = "0"
    }, 200)
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
    setTimeout(function () {
        visibleFourth.style.display = "flex"
        visibleFifth.style.display = "none"
        visibleFifthTitle.style.top = "16%"
        visibleFifthTitle.style.opacity = "0"
        visibleFifthContents.style.top = "56%"
        visibleFifthContents.style.opacity = "0"
    }, 200)
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
    setTimeout(function () {
        visibleFifth.style.display = "flex"
        visibleSixth.style.display = "none"
        visibleSixthTitle.style.top = "16%"
        visibleSixthTitle.style.opacity = "0"
        visibleSixthContents.style.top = "56%"
        visibleSixthContents.style.opacity = "0"
    }, 200)
}