function essentail(essentailCheck){
    for (i = 0; i < essentailCheck.length; i++){
        if(essentailCheck[i].value === ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
}