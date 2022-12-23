const fileListAdd = document.querySelector(".basic_file-list")
const fileList = document.querySelector(".notice_create_file_list")

let saveFile = ""

fileListAdd.addEventListener("change", fileListAddFtn)

function fileListAddFtn() {

    if (saveFile.length >= 1) {
        const dataTranster = new DataTransfer();
        let files = saveFile
        let fileArray = Array.from(files)
        let newFiles = this.files
        let newFileArray = Array.from(newFiles)
        let resultArray = fileArray.concat(newFileArray)
        resultArray.forEach(file => { dataTranster.items.add(file); });
        fileListAdd.files = dataTranster.files;
        saveFile = fileListAdd.files
    } else {
        saveFile = this.files
    }

    for (i = 0; i < this.files.length; i++) {
        const fileBox = document.createElement("div")
        fileBox.setAttribute("class", "notice_file_cell")
        fileList.appendChild(fileBox)

        const fileBoxDelete = document.createElement("div")
        fileBoxDelete.setAttribute("class", "notice_delete_file_Btn")
        fileBoxDelete.innerText = "ⅹ"
        fileBox.appendChild(fileBoxDelete)

        const fileBoxName = document.createElement("span")
        fileBoxName.innerText = this.files[i].name
        fileBox.appendChild(fileBoxName)
    };

    const loadFile = document.querySelectorAll(".notice_delete_file_Btn")

    for (i = 0; i < loadFile.length; i++) {
        loadFile[i].addEventListener("click", deleteFileFtn)
    };

    function deleteFileFtn() {
        this.parentNode.remove()
        let deleteCount = 0
        const dataTranster = new DataTransfer();
        for (i = 0; i < fileListAdd.files.length; i++) {
            if (fileListAdd.files[i].name === this.parentNode.children[1].innerText) {
                deleteCount = i
            }
        };
        let files = fileListAdd.files
        let fileArray = Array.from(files)
        let spliceFileArray = fileArray.splice(deleteCount, 1)
        fileArray.forEach(file => { dataTranster.items.add(file); });
        fileListAdd.files = dataTranster.files;
    }
}
