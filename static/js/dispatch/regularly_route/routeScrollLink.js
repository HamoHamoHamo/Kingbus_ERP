const RouteListHeadScroll = document.querySelector(".RouteListHeadScroll")
const RouteListScroll = document.querySelector(".RouteListScroll")

RouteListScroll.addEventListener("scroll", scrollLink)

function scrollLink() {
    RouteListHeadScroll.scrollLeft = RouteListScroll.scrollLeft
}