$(document).ready(function(){
  $(".accounting_outlay_welfare_bottom_box").click(function(){
    if($(".accounting_outlay_welfare_meddle_box_bottom_line_radio").css("visibility") == "hidden"){
       $(".accounting_outlay_welfare_meddle_box_bottom_line_radio").css({
        "visibility" : "inherit"
      });
      $(".accounting_outlay_welfare_bottom_box_pick").css({
        "display" : "block"
      });
    }else{
      $(".accounting_outlay_welfare_meddle_box_bottom_line_radio").css({
        "visibility" : "inherit"
      });
    }
  });
});