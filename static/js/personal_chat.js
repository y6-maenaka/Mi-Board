$(function(){

  $('#add_talker_page_bg').hide();

  $('.indicate_add_talker_page').click(function(){
    $('#add_talker_page_bg').fadeIn(300);
    $.ajax({
      type:'GET',
      url:'/personal_chat/add_talker',
      success:function(response){
        for(var key in response.new_talker_list){
          var user_list = '<li class="user_card"><a href="/friend/'+response.new_talker_list[key].user_id+'" id="user_infomation_link"><img src="/media/'+response.new_talker_list[key].user_icon_image+'" id="new_talker_icon"><div id="user_infomation"><p class="new_talker_affiliation">'+response.new_talker_list[key].university+' | '+response.new_talker_list[key].department+'</p><h1 class="new_talker_username">'+response.new_talker_list[key].last_name+' '+response.new_talker_list[key].first_name+'</h1></div></a><a href="/personal_chat/register_talker/'+response.new_talker_list[key].user_id+'" class="add_talker_btn">新規登録</a></li>'
          $('#select_new_talker_ul').append(user_list).trigger('create')
        }

      },
      error:function(response){
        console.log('error')
      }
    })
  })

  $('.get_message_anker').click(function(){

    try{
      $('.user_name_display_area').empty()
    }catch{
      console.log('')
    }

    $('#message_display_area').empty()
    var talker_id = $(this).attr('id')

    let chatSocket = new WebSocket(
      'ws://'+window.location.hostname+
      ':8001/ws/personal_chat/'+talker_id+'/');

    console.log(window.location.host)

    chatSocket.onmessage = function(e){
      var data = JSON.parse(e.data);
      var message = data['message']
      var send_user_id = data['send_user_id']

      if(send_user_id == $('#user_id_message').val()){
        var new_message = '<div class="message_container_me message_container"><p class="message_me message" >'+message+'</p></div>'
      }else{
        var new_message = '<div class="message_container_friend message_container" ><p class="message_friend message">'+message+'</p></div>'
      }

      $('#message_display_area').append(new_message).trigger('create');

      const messageDetails = document.getElementById('message_display_area')
      messageDetails.scrollTop = messageDetails.scrollHeight

    };

    chatSocket.onclose = function(e){
      console.error('chat socket closed unexpectedly')
    };


    $('#send_message_input').keypress(function(e){
      var message = $('#send_message_input').val()
      if(e.keyCode == 13 && message.length > 1){
        $('#send_message_input').val('')
        chatSocket.send(JSON.stringify({
          'message':message,
          'send_user':$('#user_id_message').val(),
        }))
      }
    })

    $('.get_message_anker').click(function(){
      try{
        chatSocket.close(1000,'change socket')
        return false;
      }catch{
        console.log('not yet open socket')
        return false;
      }
    })


    $.ajax({
      type:'GET',
      url:'/personal_chat/get_message/'+talker_id+"/",
      data:{
        'talker_id':talker_id,
      },
      success:function(response){
        for(var key in response.message_list){
          if(response.message_list[key].send_user_id ==$('#user_id_message').val()){
            var yet_message = '<div class="message_container_me message_container"><p class="message_me message" >'+response.message_list[key].message+'</p></div>'
          }else{
            var yet_message = '<div class="message_container_friend message_container" ><p class="message_friend message" >'+response.message_list[key].message+'</p></div>'
          }
          $('#message_display_area').append(yet_message).trigger('create');
        }

        if(response.talker_data[0].user_icon_image){
          var talker_name = '<a href="/friend/'+response.talker_data[0].user_id+'/" style="display:flex; align-items:center; text-decoration:none; color:black;"><img id="talking_user_icon" src="/media/'+response.talker_data[0].user_icon_image+'"><h1 class="talking_user_name" style="font-size: 0.8vw; font-weight:bold;">'+response.talker_data[0].last_name+''+response.talker_data[0].first_name+'</h1></a>'
        }else{
          var talker_name = '<a href="/friend/'+response.talker_data[0].user_id+'/" style="display:flex; align-items:center; text-decoration:none; color:black;"><img id="talking_user_icon" src="/static/image/user.svg"><h1 class="talking_user_name" style="font-size: 0.8vw; font-weight:bold;">'+response.talker_data[0].last_name+''+response.talker_data[0].first_name+'</h1></a>'
        }
        $('.user_name_display_area').append(talker_name).trigger('create');

        const messageDetails = document.getElementById('message_display_area')
        messageDetails.scrollTop = messageDetails.scrollHeight
      },
      error:function(response){
        console.log('error')
      }
    })
  })

  $(document).on('input','#search_talker_input',function(e){
    $.ajax({
      type:'POST',
      url:'/personal_chat/add_talker/',
      data:{
        input_word:$('#search_talker_input').val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      },
      success:function(response){
        for(var key in response.found_talker_list){
          $('.user_card').remove()
          var user_list = '<li class="user_card"><a href="/friend/'+response.found_talker_list[key].user_id+'" id="user_infomation_link"><img src="/media/'+response.found_talker_list[key].user_icon_image+'" id="new_talker_icon"><div id="user_infomation"><p class="new_talker_affiliation">'+response.found_talker_list[key].university+' | '+response.found_talker_list[key].department+'</p><h1 class="new_talker_username">'+response.found_talker_list[key].last_name+' '+response.found_talker_list[key].first_name+'</h1></div></a><a href="/personal_chat/register_talker/'+response.found_talker_list[key].user_id+'" class="add_talker_btn">新規登録</a></li>'
          $('#select_new_talker_ul').append(user_list).trigger('create')
        }
        console.log('ajax successs')
      },
      error:function(response){
        console.log('error')
      }
    })
  })

  $(document).on('click',function(e) {
     if(!$(e.target).closest('#select_new_talker_ul').length && $(e.target).closest('#add_talker_page_bg').length) {
       // ターゲット要素の外側をクリックした時の操作
       $('#add_talker_page_bg').fadeOut(300)
       $('.user_card').remove()
     } else {
       // ターゲット要素をクリックした時の操作
     }
  });

})



// response.new_talker_list[key]['follower_id']
