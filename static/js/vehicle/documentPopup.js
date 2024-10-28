const openDocumentPopupBtn = document.querySelectorAll('.openDocumentPopupBtn')
const documentLabel = document.querySelectorAll(".popupContainerDocument .popupArticleLabel")
const documentSendToHidden = document.querySelector(".documentSendToHidden")
const documentFiles = document.querySelectorAll(".documentFile")
const documentDeleteBtn = document.querySelectorAll(".documentDeleteBtn")

Array.from(openDocumentPopupBtn).forEach(item => item.addEventListener("click", openDocumentPopup))


function openDocumentPopup() {
    popupAreaModules[3].style.display = "block"
    documentSendToHidden.value = this.parentNode.classList[0];

    const datas = fileDatas[this.parentNode.classList[1]];
 
    
    for (i = 0; i < documentLabel.length; i++) {
        let type = documentLabel[i].innerText;
        let label = documentLabel[i];
        
        // 초기화
        label.nextElementSibling.children[2].value = ''
        label.nextElementSibling.children[4].value = ''
    
        for (j = 0; j < datas.length; j++) {
          let data = datas[j];
          if (data['type'] == type) {
            // console.log("AAAAA",data)
            console.log("AAAAA",label.nextElementSibling.children[4])
            label.nextElementSibling.children[2].value = data['filename']
            label.nextElementSibling.children[2].addEventListener("click", () => getDownloadUrl(data))
            label.nextElementSibling.children[4].value = data['id']
            break
          }
        }
    }
}


function getDownloadUrl(data) {
    window.open(`document/image/${data['id']}`, data['type'], "width=630, height=891")
}

//파일명 변경
for (i = 0; i < documentFiles.length; i++) {
    documentFiles[i].addEventListener('change', changeFileText)
}

function changeFileText() {
    console.log("TEST", this.nextElementSibling, this.files[0].name)
    this.nextElementSibling.value = this.files[0].name
    // console.log("tset", this.parentNode.children[4])
    // 삭제용 name값 초기화
    this.parentNode.children[4].name = ''

}

// 파일삭제
for (i = 0; i < documentDeleteBtn.length; i++) {
    documentDeleteBtn[i].addEventListener('click', deleteFile)
}

function deleteFile() {
    this.previousElementSibling.previousElementSibling.value = ""
    this.previousElementSibling.value = ""
    this.nextElementSibling.name = "delete_file_id"
    console.log(this.nextElementSibling)
}
  