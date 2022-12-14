const openMenu = document.querySelectorAll(".have_menu_list")

for (i = 0; i < openMenu.length; i++){
    openMenu[i].parentNode.addEventListener("click", openMenuFtn)
};

function openMenuFtn(){
    if(this.nextElementSibling.classList.contains("menu_box-depth2-open")){
        for (i = 0; i < openMenu.length; i++){
            closeMenuFtn(openMenu[i])
        };
    }else{
        for (i = 0; i < openMenu.length; i++){
            closeMenuFtn(openMenu[i])
        };
        this.nextElementSibling.classList.add("menu_box-depth2-open")
        if(screen.width > 1920){
            this.nextElementSibling.style.maxHeight = `${this.nextElementSibling.children.length*4}rem`
        }else if(screen.width <= 1920 && screen.width > 1680){
            this.nextElementSibling.style.maxHeight = `${this.nextElementSibling.children.length*4}rem`
        }else{
            this.nextElementSibling.style.maxHeight = `${this.nextElementSibling.children.length*3.6}rem`
        }
        this.classList.add("menu_item-open")
        this.children[0].children[0].children[0].classList.add("open_white")
        this.children[2].children[0].children[0].classList.add("open_white")
        this.children[2].classList.add("menu_open_btn-open")
    }
}

function closeMenuFtn(targetMemu){
    targetMemu.parentNode.nextElementSibling.classList.remove("menu_box-depth2-open")
    targetMemu.parentNode.nextElementSibling.style.maxHeight = "0"
    targetMemu.parentNode.classList.remove("menu_item-open")
    targetMemu.parentNode.children[0].children[0].children[0].classList.remove("open_white")
    targetMemu.parentNode.children[2].children[0].children[0].classList.remove("open_white")
    targetMemu.parentNode.children[2].classList.remove("menu_open_btn-open")
}