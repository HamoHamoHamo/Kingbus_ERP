class Comma {
    static addCommaToInnerText = () => {
        console.log("addCommaToInnerText")
        const addComma = document.querySelectorAll(".addCommaToInnerText")
        for (i = 0; i < addComma.length; i++){
            console.log("TESt")
            addComma[i].innerText = addComma[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        };
    }

    static inputComma() {
        console.log("add InputComma")
        const inputComma = document.querySelectorAll('.inputComma')
        Array.from(inputComma).forEach(item => {
            item.value = item.value?.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
            item.addEventListener("blur", (e) => {
                e.target.value = e.target.value?.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
            })
            item.addEventListener("click", (e) => {
                e.target.value = e.target.value?.replace(/\,/g, "");
            })
        })
    }
}


export { Comma }