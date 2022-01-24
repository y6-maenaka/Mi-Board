$(function(){

 var ua = navigator.userAgent;
  if(ua.indexOf("iPhone") > 0 || ua.indexOf("Android") > 0 && ua.indexOf("Mobile") > 0){
  }else{

    $('.global_menu_item_link').hover(function(){
      icon_name = $(this).attr('id')

          $("."+icon_name).css({'display':'flex','font-size':'0.8rem','background':'gray','color':'#ffffff','padding':'1vh 0.6vw','border-radius':'5px','z-index':'300'})
    },
    function(){
      $("."+icon_name).css('display','none')
    })

  var url = new URL(window.location.href);
  var params = url.pathname.split('/')[1];

  switch(params){
    case 'mypage':
      $('#global_menu_item_mypage').attr('class','selected')
      break;

    case 'friend':
      $('#global_menu_item_friend').attr('class','selected')
      break;

    case 'room':
      $('#global_menu_item_room').attr('class','selected')
      break;

    case 'board':
      $('#global_menu_item_board').attr('class','selected')
      break;

    case 'personal_chat':
      $('#global_menu_item_personal_chat').attr('class','selected')
      break;

    case 'stoppo':
      $('#global_menu_item_stoppo').attr('class','selected')
      break;

  }
 }
 $('#notification_bell').click(function(){
   $('#notification_box_bg').fadeIn(200)
   $.ajax({
     type:'GET',
     url:'/notification/checked_notification/',
     success:function(response){
     },
     error:function(response){
     }
   })
 })

 $(document).on('click',function(e) {
    if(!$(e.target).closest('#notification_box').length && $(e.target).closest('#notification_box_bg').length) {
      // ターゲット要素の外側をクリックした時の操作
      $('#notification_box_bg').fadeOut(300)
    } else {
      // ターゲット要素をクリックした時の操作
    }
 });

 $('#notification_box_bg').hide()
 $('#communication_state_unstable_bg').hide()

 Push.Permission.request();
 var notification_sound = new Audio('/static/image/notification_sound.mp3');

  var notificationSocket = new WebSocket(
    'wss://'+window.location.hostname+
    ':8001/ws/notification/');


    notificationSocket.onmessage = function(e){
      notification_sound.play();
      notification_sound.currentTime = 0;
      var data = JSON.parse(e.data);
      if(data['send_user_id'] == $('#notification_user_id').val()){
      }else{
        Push.create('Mi-Board', {
        　　body: ''+data.notification_detail+'から新しい通知があります',
        　　icon: '/static/image/mi-board-logo.png',
        　　timeout: 8000, // 通知が消えるタイミング
        　　vibrate: [100, 100, 100], // モバイル端末でのバイブレーション秒数
        　　onClick: function() {
        　　　　// 通知がクリックされた場合の設定
        　　}
        });

      var notification = '<div class="notification_card"><p>From '+data.notification_detail+'</p><h1>新しいメッセージがあります</h1><img class="notification_logo" src="/static/image/mi-board-logo.png"></div>'
      setTimeout(() => {
        $('.notification_card').fadeOut(100)
        notification_sound.pause();
        // $('.notification_area').empty();
      }, 4000);
    }

    $('.notification_area').append(notification)

    }

    notificationSocket.onopen = function(e){
    }


    notificationSocket.onclose = function(e){
      $('#communication_state_unstable_bg').fadeIn(100)


    }

});
