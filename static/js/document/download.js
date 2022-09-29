const downloadBtn = document.querySelector(".download")
const fileCheck = document.querySelectorAll(".fileCheck")
const contentsAreaBox = document.querySelector(".contentsAreaBox")

downloadBtn.addEventListener("click", download)

function download() {
    for (i = 0; i < fileCheck.length; i++) {
        if (fileCheck[i].checked) {
            const blob = new Blob([this.content], { type: 'text/plain' })
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement("a")
            a.href = url
            a.download = `${fileCheck[i].classList[2]}`
            a.click()
            a.remove()
            window.URL.revokeObjectURL(url);
        }
    }
}