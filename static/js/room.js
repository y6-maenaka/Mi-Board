$(function(){


  var room_id = $('#message_room_id').val()

  $.ajax({
    type:'GET',
    url:'/room/get_message/'+room_id+'/',
    data:{
      'room_id':room_id,
    },
    success:function(response){
      for(var key in response.message_list){
        if(response.message_list[key].send_user_id == $('#message_user_id').val()){
          var yet_message = '<div class="message_container message_container_me"><p class="message message_me">'+response.message_list[key].message+'</p></div>'
        }else{
          var yet_message = '<div class="message_container message_container_other"><p class="message message_other">'+response.message_list[key].message+'</p></div>'
        }
        $('#room_chat').append(yet_message).trigger('create')

        const messageDetails = document.getElementById('room_chat')
        messageDetails.scrollTop = messageDetails.scrollHeight
      }
    },
    error:function(response){
    }
  })


  var roomChatSocket = new WebSocket(
    'ws://'+window.location.hostname+
    ':8001/ws/room_chat/'+room_id+'/');

  roomChatSocket.onmessage = function(e){
    var data = JSON.parse(e.data);
    var message = data['message']
    var send_user_id = data['send_user_id']

    if(send_user_id == $('#message_user_id').val()){
      var new_message = '<div class="message_container message_container_me"><p class="message message_me">'+message+'</p></div>'
    }else{
      var new_message = '<div class="message_container message_container_other"><p class="message message_other">'+message+'</p></div>'
    }
    $('#room_chat').append(new_message)
    const messageDetails = document.getElementById('room_chat')
    messageDetails.scrollTop = messageDetails.scrollHeight
  }

  roomChatSocket.onclose = function(e){
  }

  $('#send_message_input_room').keypress(function(e){
    var message = $(this).val()
    if(e.keyCode == 13 && message.length > 1){
      $(this).val('')
      roomChatSocket.send(JSON.stringify({
        'message':message,
        'send_user':$('#message_user_id').val(),
      }))
    }
  })


  $('#create_room_page_bg').hide();
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
    var work_time = $('#work_time_input').val()
    var week_at = $('#week_at').val()

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
  });

  $('.btn-change_relation').click(function(){
    var state = $(this).attr('id');
    var room_id = $(this).val();

    $.ajax({
      type : 'GET',
      url : '/discover/change_relation_room',
      data : {
        state : state,
        room_id : room_id,
      },

      success:function(response){
        if(state == 'secession'){
          $('.'+room_id).attr('id','join')
          $('.'+room_id).html('参加')
        }else{
          $('.'+room_id).attr('id','secession')
          $('.'+room_id).html('退会')
        }
      },
      error:function(response){
      }
    })
  })

  $('#post_ground_modal_bg').hide()

  $('#post_ground_btn').click(function(){
    $('#post_ground_modal_bg').fadeIn(300);
  })

  $('#ground_image_input').on('change',function(e){
    var reader = new FileReader();
    reader.onload = function(e){
      $('#preview_post_image').attr('src', e.target.result);
    }
    reader.readAsDataURL(e.target.files[0]);
    $('.ground_image_input_label p').html('変更')
  });

  function confirm_view_board(){
    if(!confirm("ポイントを使ってこの記事を取得しますか？　※すでに取得済みの場合、コイン消費はありません")){
      return false;
    }else{
    }
  }

  $('.related_board_article').click(function(){
    confirm_view_board()
  })

  $('.related_board_article_content').click(function(){
    confirm_view_board()
  })

  $('.related_board_article_attached_file').click(function(){
    confirm_view_board()
  })

  $('.related_board_article_image').click(function(){
    confirm_view_board()
  })

  $('.related_article_board_image_link').click(function(){
    confirm_view_board()
  })

  $('#post_board_page_bg').hide()

  $('#dummy_input_board').click(function(){
    $('#post_board_page_bg').fadeIn(300);
  })

  $(document).on('click',function(e) {
     if(!$(e.target).closest('#post_board_page').length && $(e.target).closest('#post_board_page_bg').length) {
       // ターゲット要素の外側をクリックした時の操作
       $('#post_board_page_bg').fadeOut(300)
     } else {
       // ターゲット要素をクリックした時の操作
     }
  });

  $('#btn-copy-link').click(function(){
    alert('現在この機能はお使いいただけません')
  })
})
