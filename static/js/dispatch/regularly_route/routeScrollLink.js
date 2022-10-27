const RouteListHeadScroll = document.querySelector(".RouteListHeadScroll")

RouteListScroll.addEventListener("scroll", scrollLink)

function scrollLink() {
    RouteListHeadScroll.scrollLeft = RouteListScroll.scrollLeft
}