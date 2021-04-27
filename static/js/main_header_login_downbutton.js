$(document).ready(function(){
    $(".basic_header_profile_button").click(function(){
      if($(".profile_underbox_form").css("display") == "none"){
         $(".profile_underbox_form").css({
          "display" : "block"
        });
      }else{
        $(".profile_underbox_form").css({
          "display" : "none"
        });
      }
    });
  });