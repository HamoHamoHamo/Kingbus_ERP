const fileInput = document.querySelectorAll(".basic_file")

for (i = 0; i < fileInput.length; i++){
    fileInput[i].addEventListener("change", loadFileFtn)
};

function loadFileFtn(){
    let fileName = ""
    for (i = 0; i < this.files.length; i++){
        fileName  = `${fileName} ${this.files[i].name}`
    };
        this.parentNode.children[2].value = fileName
}