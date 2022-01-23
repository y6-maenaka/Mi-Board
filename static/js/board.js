$(function(){
  $('.evaluation_bg').hide()

  $('#evaluation_btn').click(function(){
    $('.evaluation_bg').fadeIn(300);
    return false
  })

  $('.commented_user_item').click(function(){

    $.ajax({
      type:'GET',
      url:'/board/evaluation/',
      data:{
        'board_id':$('.board_id').val(),
        'evaluation_user_id':$('.commented_user_item').attr('name'),
        'comment_id':$('.comment_id').val(),
        'bet_points':$('.bet_points').val(),
      },
      success:function(response){
        location.reload();
      },
      error:function(response){
      }
    })
  })

  $('.article_link').click(function(){
    var bet_points = $('#board_bet_points').val()
    if(!confirm(""+bet_points+"で記事を取得しますか？　※すでに購入済みの場合、コイン消費はありません")){
      return false;
    }else{
    }
  });

  $('#like_btn').click(function(){
    var state = $(this).attr('class')
    $.ajax({
      type:'GET',
      url:'/board/good_board/',
      data:{
        'board_id':$('.board_id').val(),
        'state':state,
      },
      success:function(response){
        if(state=='non_executed'){
          $('#like_btn').attr('class','executed')
        }else{
          $('#like_btn').attr('class','non_executed')
        }
      },
      error:function(response){
      }
    })
  })

  $('#store_btn').click(function(){
    var state = $(this).attr('class')
    $.ajax({
      type:'GET',
      url:'/board/store_board/',
      data:{
        'board_id':$('.board_id').val(),
        'state':state,
      },
      success:function(response){
        if(state == 'non_executed'){
          $('#store_btn').attr('class','executed')
        }else{
          $('#store_btn').attr('class','non_executed')
        }
      },
      error:function(response){
      }
    })
  })

  $(document).on('click',function(e) {
     if(!$(e.target).closest('.evaluation_page').length && $(e.target).closest('.evaluation_bg').length) {
       // ターゲット要素の外側をクリックした時の操作
       $('.evaluation_bg').fadeOut(300)
     } else {
       // ターゲット要素をクリックした時の操作
     }
  });

})
