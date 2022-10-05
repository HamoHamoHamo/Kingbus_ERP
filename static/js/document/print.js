const printBtn = document.querySelector(".print")

printBtn.addEventListener("click", printing)


function printing(){
    for (i = 0; i < fileCheck.length; i++) {
        let printTarget = fileCheck[i].parentNode.parentNode.children[1]
        if (fileCheck[i].checked) {
            if(printTarget.innerText.substr(-4).split(".")[1] !== "zip"
            && printTarget.innerText.substr(-4).split(".")[1] !== "exe"
            && printTarget.innerText.substr(-4).split(".")[1] !== "avi"
            && printTarget.innerText.substr(-4).split(".")[1] !== "flv"
            && printTarget.innerText.substr(-4).split(".")[1] !== "mkv"
            && printTarget.innerText.substr(-4).split(".")[1] !== "mov"
            && printTarget.innerText.substr(-4).split(".")[1] !== "mp3"
            && printTarget.innerText.substr(-4).split(".")[1] !== "mp4"
            && printTarget.innerText.substr(-4).split(".")[1] !== "wav"
            && printTarget.innerText.substr(-4).split(".")[1] !== "wma"
            ){
                let openPopup = window.open(`${fileCheck[i].classList[2]}`,"프린트팝업", width=100, height=60)
            }else{
                alert('파일형식이 올바르지 않습니다.')
            }
        }
    }
}