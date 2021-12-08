$(function(){
  $('.change_user_icon_image').on('change',function(e){
    var reader = new FileReader();
    console.log('sucee')
    reader.onload = function(e){
      $('#before_user_icon_image').attr('src',e.target.result);
    }
    reader.readAsDataURL(e.target.files[0]);
  });

  $('.change_user_background_image').on('change',function(e){
    var reader = new FileReader();
    console.log('sucee')
    reader.onload = function(e){
      $('#before_user_background_image').attr('src',e.target.result);
    }
    reader.readAsDataURL(e.target.files[0]);
  });
})
