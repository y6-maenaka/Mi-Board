$(function(){
  $('#post_ground_modal_bg').hide()

  $('#post_ground_btn').click(function(){
    $('#post_ground_modal_bg').fadeIn(300);
  })

  $('#ground_image_input').on('change',function(e){
    console.log('change')
    var reader = new FileReader();
    reader.onload = function(e){
      $('#preview_post_image').attr('src', e.target.result);
    }
    reader.readAsDataURL(e.target.files[0]);
    $('.ground_image_input_label p').html('変更')
  });
})
