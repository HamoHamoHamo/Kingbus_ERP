const addCommaToInnerText = () => {
    const addComma = document.querySelectorAll(".addCommaToInnerText")

    for (i = 0; i < addComma.length; i++){
        addComma[i].innerText = addComma[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };
}

export { addCommaToInnerText }