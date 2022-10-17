const input= document.querySelectorAll(".inputCell input")
const nextStepBtn = document.querySelector(".nextStepBtn")
const cTel = document.querySelector("#cTel")
const tel = document.querySelector("#tel")
const businessCord = document.querySelector("#businessCord")
const signupHeaderTitle = document.querySelector(".signupHeaderTitle")
const email = document.querySelector("#email")

nextStepBtn.addEventListener("click", nextBtn)

let regPhone = /^([0-9]{2,3})-?([0-9]{3,4})-?([0-9]{4})$/;
let regBusinessCord = /^([0-9]{3})-?([0-9]{2})-?([0-9]{5})$/;

function nextBtn(event) {
  if (input[0].value == "" || input[1].value == "" || input[2].value == "" || input[3].value == "" || input[4].value == "" || input[5].value == "" || input[6].value == "" || input[7].value == "" || input[8].value == "" || input[9].value == "") {
    alert("입력되지 않은 항목이 있습니다.")
    event.preventDefault();
  } else if (input[0].attributes.check_result.value == "fail") {
    alert("아이디 중복확인이 되지 않았습니다.")
    event.preventDefault();
  } else if (input[1].value !== input[2].value) {
    alert("비밀번호 확인을 다시 진행해 주세요.")
    event.preventDefault();
  } else if (regPhone.test(cTel.value) !== true) {
    alert("회사 전화번호가 올바르지 않습니다.")
    event.preventDefault();
  } else if (regBusinessCord.test(businessCord.value) !== true) {
    alert("사업자등록번호가 올바르지 않습니다.")
    event.preventDefault();
  } else if (regPhone.test(tel.value) !== true) {
    alert("담당자 전화번호가 올바르지 않습니다.")
    event.preventDefault();
  } else if (!email.value.includes('@') || !email.value.includes('.') || email.value.includes(' ')) {
    alert("이메일이 올바르지 않습니다.")
    event.preventDefault();
  }
}


signupHeaderTitle.addEventListener("click", check)

function check() {
  console.log(regPhone.test(cTel.value))
}






// 아이디 중복검사
function id_overlap_check() {

  $('.username_input').change(function () {
    $('#id_check_sucess').hide();
    $('.id_overlap_button').show();
    $('.username_input').attr("check_result", "fail");
  })


  if ($('.username_input').val() == '') {
    alert('이메일을 입력해주세요.')
    return;
  }

  id_overlap_input= document.querySelector('input[name="user_id"]');

  $.ajax({
    url: "/member/id-check",
    data: {
      'user_id': id_overlap_input.value
    },
    datatype: 'json',
    success: function (data) {
      console.log(data['overlap']);
      if (data['overlap'] == "fail") {
        alert("이미 존재하는 아이디 입니다.");
        id_overlap_input.focus();
        return;
      } else {
        alert("사용가능한 아이디 입니다.");
        $('.username_input').attr("check_result", "success");
        $('#id_check_sucess').show();
        $('.id_overlap_button').hide();
        return;
      }
    },
    error: function (request, status, error) {
      console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
      // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
    }
  });
}

/////////////////아이디

// if ($('.username_input').attr("check_result") == "fail"){
//   alert("아이디 중복체크를 해주시기 바랍니다.");
//   $('.username_input').focus();
//   return false;
// }