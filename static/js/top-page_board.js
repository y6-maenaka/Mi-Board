$(function(){
  // $('#post_board_page_bg').hide();


  $('.post_board').click(function(){
    $('#post_board_bg').fadeIn(300);
  })



  $('.btn_submit_board_data').click(function(){
    $('#post_board_bg').fadeOut(300);
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
     if(!$(e.target).closest('#post_board_form').length && $(e.target).closest('#post_board_bg').length) {
       // ターゲット要素の外側をクリックした時の操作
       $('#post_board_bg').fadeOut(300)
     } else {
       // ターゲット要素をクリックした時の操作
     }
  });


})
