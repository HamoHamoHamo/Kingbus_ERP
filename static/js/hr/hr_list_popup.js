const openPopup = document.getElementById('popupButton');
const container = document.getElementById('hrPopupContainer');
const closePopup = document.getElementById('hrPopupoutlay');
const closePopupButton = document.getElementById('closePopupButton');
const selector = $('.popup_member_tr');
const inputMemberId = $('#input_member_id');

openPopup.addEventListener('click', function(){
  container.style.display = 'block';
});

closePopup.addEventListener('click', function(){
 container.style.display = 'none';
});

closePopupButton.addEventListener('click', function(){
  container.style.display = 'none';
 });

selector.click(function(){
  let memberId = $(this).children('.popup_member_id').val();
  let memberName = $(this).children('.hr_member_list__name').children('span').text();
  console.log(memberName);
  $(openPopup).text(memberName);
  $(inputMemberId).val(memberId);
  container.style.display = 'none';
});