$(function(){
  // $('#post_board_page_bg').hide();

  window.onkeydown = function(e) {
  if (e.keyCode == 9)
    return false; // Disable Tab!
}

  $('.post_board').click(function(){
    $('#post_board_page_bg').fadeIn(300);
  })

  $('.btn_go_next_page').click(function(){
    var input_title = $('#input_title').val()
    var input_content = $('#input_content').val()
    var input_tags = $('#input_tags').val()
    var input_display_name = $('input[type="radio"]:checked').val()
    var input_bet_points = $('#input_bet_points').val()
    var input_category = $('#input_category').val()
    var input_related_department = $('#input_related_department').val()

    console.log(input_display_name)
    if(input_display_name == 'real_name'){
      input_display_name = '実名'
    }else{
      input_display_name = '匿名'
    }

    $('#confirm_title').append(input_title)
    $('#confirm_content').append(input_content)
    $('#confirm_tags').append(input_tags)
    $('#confirm_category').append(input_category)
    $('#confirm_bet_points').append(input_bet_points)
    $('#confirm_display_name').append(input_display_name)
    $('#confirm_related_department').append(input_related_department)
    $('.post_board_form').animate({'left':'-30vw'})
  })

  $('#cancel_btn').click(function(){
    $('#post_board_page_bg').fadeOut(300);
  })

  $('.back_to_post_form_input').click(function(){
    $('.post_board_form').animate({'left':'0'});
    $('.confirm_item').html('')
  })

  $('.btn_submit_board_data').click(function(){
    $('#post_board_page_bg').fadeOut(300);
  })

  $('.search_word').click(function(){
    $('#search_box_board').val($(this).html())
  })

  $('.article_link').click(function(){
    var bet_points = $('#board_bet_points').val()
    if(!confirm("ポイントを使ってこの記事を取得しますか？　※すでに取得済みの場合、コイン消費はありません")){
      return false;
    }else{
      console.log('ok')
    }
  });

  $(document).on('click',function(e) {
     if(!$(e.target).closest('.slide_item').length && $(e.target).closest('#post_board_page_bg').length) {
       // ターゲット要素の外側をクリックした時の操作
       $('#post_board_page_bg').fadeOut(300)
     } else {
       // ターゲット要素をクリックした時の操作
     }
  });


})
