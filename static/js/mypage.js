$(function(){


    $(document).on('click',function(e) {
       if(!$(e.target).closest('.link_container_room_image').length && $(e.target).closest('.spot').length) {
         $('.register_room_modal_bg').fadeIn(300)
       }



    var spot_num = $(this).attr('id')
    $.ajax({
      type : 'GET',
      url : '/mypage/set_room/',
      data:{
        spot_num:spot_num
      },
      success:function(response){
        var cancel_add_room = '<li class="cancel_add_room"><a href="/mypage/remove_seted_room/?spot='+spot_num+'/">取り消し</a></li>'
        $('.register_room_modal').append(cancel_add_room)
        if(response.match_room_list !== null){
          for(var key in response.match_room_list){
            if(response.match_room_list[key].room_image){
            var match_room_card = '<li class="recomend_room_card"><div class="room_card_img_detail_container"><img id="room_card_img" src="/media/'+response.match_room_list[key].room_image+'"><div class="room_card_detail_container"><p>'+response.match_room_list[key].university+'|'+response.match_room_list[key].subject_to+'</p><h1>'+response.match_room_list[key].room_name+'</h1></div></div><a id="btn_room_set" href="/mypage/add_room_timetable/'+response.match_room_list[key].room_id+'?spot='+spot_num+'/">登録する</a></li>'
          }else{
            var match_room_card = '<li class="recomend_room_card"><div class="room_card_img_detail_container"><img id="room_card_img" src="/static/image/room.svg"><div class="room_card_detail_container"><p>'+response.match_room_list[key].university+'|'+response.match_room_list[key].subject_to+'</p><h1>'+response.match_room_list[key].room_name+'</h1></div></div><a id="btn_room_set" href="/mypage/add_room_timetable/'+response.match_room_list[key].room_id+'?spot='+spot_num+'/">登録する</a></li>'
          }
            $('.register_room_modal').append(match_room_card)
          }
        }
        for(var key in response.recomend_room_list){
          if(response.recomend_room_list[key].room_image){
            var recomend_room_card = '<li class="recomend_room_card"><div class="room_card_img_detail_container"><img id="room_card_img" src="/media/'+response.recomend_room_list[key].room_image+'"><div class="room_card_detail_container"><p>'+response.recomend_room_list[key].university+'|'+response.recomend_room_list[key].subject_to+'</p><h1>'+response.recomend_room_list[key].room_name+'</h1></div></div><a id="btn_room_set" href="/mypage/add_room_timetable/'+response.recomend_room_list[key].room_id+'?spot='+spot_num+'/">登録する</a></li>'
          }else{
            var recomend_room_card = '<li class="recomend_room_card"><div class="room_card_img_detail_container"><img id="room_card_img" src="/static/image/room.svg"><div class="room_card_detail_container"><p>'+response.recomend_room_list[key].university+'|'+response.recomend_room_list[key].subject_to+'</p><h1>'+response.recomend_room_list[key].room_name+'</h1></div></div><a id="btn_room_set" href="/mypage/add_room_timetable/'+response.recomend_room_list[key].room_id+'?spot='+spot_num+'/">登録する</a></li>'
          }
          $('.register_room_modal').append(recomend_room_card)
        }


      },
      error:function(response){
      }
    })

    $(document).on('input','#search_room_input',function(e){
      $.ajax({
        type: 'GET',
        url:'/mypage/search_set_room/',
        data:{
          input_word:$('#search_room_input').val()
        },
        success:function(response){
          if(response.hit_room_list !== null){
            for(var key in response.hit_room_list){
              $('.recomend_room_card').remove()
              var hit_room_card = '<li class="recomend_room_card"><div class="room_card_img_detail_container"><img id="room_card_img" src="/media/'+response.hit_room_list[key].room_image+'"><div class="room_card_detail_container"><p>'+response.hit_room_list[key].university+'|'+response.hit_room_list[key].subject_to+'</p><h1>'+response.hit_room_list[key].room_name+'</h1></div></div><a id="btn_room_set" href="/mypage/add_room_timetable/'+response.hit_room_list[key].room_id+'?spot='+spot_num+'/">登録する</a></li>'
              $('.register_room_modal').append(hit_room_card)
            }
          }
        },
        error:function(response){
        }
      })
    })
  })

  $(document).on('click',function(e) {
     if(!$(e.target).closest('.register_room_modal').length && $(e.target).closest('.register_room_modal_bg').length) {
       // ターゲット要素の外側をクリックした時の操作
       $('.register_room_modal_bg').fadeOut(300)
       $('.recomend_room_card').remove()
       $('.cancel_add_room').remove()
     } else {
       // ターゲット要素をクリックした時の操作
     }
  });

  $(document).on('click',function(e) {
     if(!$(e.target).closest('#mi_qr_container').length && $(e.target).closest('#mi_qr_bg').length) {
      $('#mi_qr_bg').fadeOut(300)
     }
   })

})
