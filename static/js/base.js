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

  var notificationSocket = new WebSocket(
    'ws://'+window.location.hostname+
    ':8001/ws/notification/');


    notificationSocket.onmessage = function(e){
      var data = JSON.parse(e.data);
      if(data['send_user_id'] == $('#notification_user_id').val()){
        console.log('')
      }else{
      var notification = '<div class="notification_card"><p>From '+data.notification_detail+'</p><h1>新しいメッセージがあります</h1><img class="notification_logo" src="/static/image/mi-board-logo.png"></div>'
      setTimeout(() => {
        $('.notification_card').fadeOut(100)
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
