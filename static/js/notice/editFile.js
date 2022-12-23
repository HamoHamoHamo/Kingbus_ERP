const editDeleteFile = document.querySelectorAll(".notice_delete_file_Btn")

for (i = 0; i < editDeleteFile.length; i++){
    editDeleteFile[i].addEventListener("click", editDeleteFileFtn)
};

function editDeleteFileFtn(){
    this.parentNode.remove()
}