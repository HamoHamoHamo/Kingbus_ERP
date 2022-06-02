$(document).ready(function(){
    var fileTarget = $('.mid_box_input_filebox .upload-hidden');
    console.log(fileTarget)
  
      fileTarget.on('change', function(){
          if(window.FileReader){
              var filename = $(this)[0].files[0].name;
          } else {
              var filename = $(this).val().split('/').pop().split('\\').pop();
          }
  
          $(this).siblings('.mid_box_upload-name').val(filename);
      });
  }); 