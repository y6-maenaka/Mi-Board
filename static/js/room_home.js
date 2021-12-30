$(function(){

  window.onkeydown = function(e) {
  if (e.keyCode == 9)
    return false; // Disable Tab!
}

  // $('#create_room_page_bg').hide();
  $('.create_room_move_modal').click(function(){
    $('#create_room_page_bg').fadeIn(300);
    return false
  });

  $('.btn-submit-room_data').click(function(){
    $('#create_room_page_bg').fadeOut(300);
  });

  var duration = 700;

  $('.btn_go_next_page').click(function(){
    var room_name_confirm = $('#room_name_input').val();
    var representative_person_name_confirm = $('#representative_person_name_input').val()
    var subject_to_confirm = $('#subject_to_input').val();
    var category = $('#category_input').val()
    var work_time_confirm = $('#work_time_input').val()
    var week_at = $('#week_at_input').val()

    $('#room_name_confirm').append(room_name_confirm)
    $('#representative_person_name_confirm').append(representative_person_name_confirm)
    $('#category_confirm').append(category)
    $('#subject_to_confirm').append(subject_to_confirm)
    $('#work_time_confirm').append(work_time_confirm)
    $('#week_at_confirm').append(week_at)
    $('.create_room_form').animate({'left':'-30vw'})

    // 作成したサイトにリダイレクトさせる
  });

  $('.back_to_create_room_page').click(function(){
    $('.create_room_form').animate({'left':'0'});
    $('.confirm_item').html('')
  });


  $(document).on('click',function(e) {
     if(!$(e.target).closest('.slide_item').length && $(e.target).closest('#create_room_page_bg').length) {
       // ターゲット要素の外側をクリックした時の操作
       $('#create_room_page_bg').fadeOut(300)
     } else {
       // ターゲット要素をクリックした時の操作
     }
  });
})
