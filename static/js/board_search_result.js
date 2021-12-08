$(function(){

  $('.article_link').click(function(){
    var bet_points = $('#board_bet_points').val()
    if(!confirm(""+bet_points+"で記事を取得しますか？　※すでに購入済みの場合、コイン消費はありません")){
      return false;
    }else{
      console.log('ok')
    }
  });

})
