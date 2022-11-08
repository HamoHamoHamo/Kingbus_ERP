function sliceLength(calnderItem){
    for (i = 0; i < calnderItem.length; i++){
        if(calnderItem[i].innerText.length > 8){
            calnderItem[i].innerText = `${calnderItem[i].innerText.substr(0,8)}...`
        }
    };
}