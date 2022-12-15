function allCheckerFtn(allChecker, checker){
    if(allChecker.checked){
        for (i = 0; i < checker.length; i++){
            checker[i].checked = true
        };
    }else{
        for (i = 0; i < checker.length; i++){
            checker[i].checked = false
        };
    }
}

function checkerFtn(allChecker, checker){
    let checkerCnt = 0
    for (i = 0; i < checker.length; i++){
        if(checker[i].checked){
            checkerCnt++
        }
    };

    if(checker.length === checkerCnt){
        allChecker.checked = true
    }else{
        allChecker.checked = false
    }
}