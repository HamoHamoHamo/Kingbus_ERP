const changePwPopup = document.querySelector(".change_pw_popup")
const pwChangeMenu = document.querySelector(".pw_change_menu")
const pwChangeBtn = document.querySelector(".pw_change_btn")
const essentialPw = document.querySelectorAll(".pw_essential")
const pwChangePw = document.querySelector(".pw_change_pw")
const pwChangeNew = document.querySelector(".pw_change_new")
const pwChangeCheck = document.querySelector(".pw_change_check")

pwChangeMenu.addEventListener("click", pwChangeFtn)

function pwChangeFtn(e) {
    e.stopPropagation()
    if(changePwPopup.style.display === "block"){
        closePopup(false, "nothing")
    }else{
        closePopup(true, "pw")
        changePwPopup.style.display = "block"
    }
}

pwChangeBtn.addEventListener("click", changePw)

function changePw(){
    for (i = 0; i < essentialPw.length; i++){
        if(essentialPw[i].value === ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    if(pwChangeNew.value !== pwChangeCheck.value){
        return alert("새 비밀번호와 비밀번호 확인이 맞지 않습니다.")
    }
    
    $.ajax({
        url: "/member/change/password",
        method: "POST",
        data: {
            'cur_password': pwChangePw.value,
            'password1': pwChangeNew.value,
            'password2': pwChangeCheck.value,
            'csrfmiddlewaretoken': csrftoken
        },
        datatype: 'json',
        success: function (data) {
            if (data['status'] == "fail") {
                alert("비밀번호가 올바르지 않습니다.");
                pwChangePw.focus();
                return;
            } else {
                alert("비밀번호가 변경되었습니다.")
                pwChangePw.value = ""
                pwChangeNew.value = ""
                pwChangeCheck.value = ""
                closePopup(false, "nothing")
                return;
            }
        },
        error: function (request, status, error) {
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
        }
    });
}