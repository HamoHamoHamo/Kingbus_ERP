const downloadBtn = document.querySelector(".download")
const fileCheck = document.querySelectorAll(".fileCheck")
const contentsAreaBox = document.querySelector(".contentsAreaBox")

downloadBtn.addEventListener("click", download)

function download() {
    let count = 0;
    for (i = 0; i < fileCheck.length; i++) {
        if (fileCheck[i].checked) {
            const a = document.createElement("a")
            a.setAttribute("href", `${fileCheck[i].classList[2]}`);
            // a.download = `${fileCheck[i].parentNode.parentNode.children[1].innerText}`
            document.body.appendChild(a);
            setTimeout(() => {
                console.log("after")
                a.click();
            }, 500*count);
            count = count + 1;   
        }
    }
}