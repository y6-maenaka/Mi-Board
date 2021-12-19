$(function(){
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

  var notificationSocket = new WebSocket(
    'ws://'+window.location.hostname+
    ':8001/ws/notification/');

    notificationSocket.onmessage = function(e){
      var data = JSON.parse(e.data);
      if(data['send_user_id'] == $('notification_user_id').val()){
        console.log('')
      }else{
      var notification = '<div class="notification_card"><p>'+data.notification_detail+'</p><h1>新しいメッセージがあります</h1></div>'
    }
      $('.notification_card').empty()
      $(window).append(notification).trigger('create')
      $('.notification_area').animate({'top':'100px'},500)

    }

    notificationSocket.onclose = function(e){
      console.error('notification socket closed unexpectedly')
    }
});
