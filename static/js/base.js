$(function(){

 var ua = navigator.userAgent;
  if(ua.indexOf("iPhone") > 0 || ua.indexOf("Android") > 0 && ua.indexOf("Mobile") > 0){
  console.log("スマートフォン用のコードを書く");
  }else{




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

    // case 'ground':
    //   $('#global_menu_item_ground').attr('class','selected')
    //   break;
  }
 }

 Push.Permission.request();
 var notification_sound = new Audio('/static/image/notification sound.mp3');

  var notificationSocket = new WebSocket(
    'ws://'+window.location.host+
    '/ws/notification/');


    notificationSocket.onmessage = function(e){
      notification_sound.play();
      notification_sound.currentTime = 0;
      var data = JSON.parse(e.data);
      if(data['send_user_id'] == $('#notification_user_id').val()){
        console.log('')
      }else{
        Push.create('Mi-Board', {
        　　body: ''+data.notification_detail+'から新しい通知があります',
        　　icon: '/static/image/mi-board-logo.png',
        　　timeout: 8000, // 通知が消えるタイミング
        　　vibrate: [100, 100, 100], // モバイル端末でのバイブレーション秒数
        　　onClick: function() {
        　　　　// 通知がクリックされた場合の設定
        　　　console.log(this);
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
      console.log('socket open')
    }


    notificationSocket.onclose = function(e){
      console.error('notification socket closed unexpectedly')
    }
});
