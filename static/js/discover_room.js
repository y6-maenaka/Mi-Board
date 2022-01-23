$(function(){
  $(document).on('click','.btn-change-relation',function(){
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

  $(document).on('input','#search_room_input',function(e){
    $.ajax({
      type: 'GET',
      url: '/discover/search_room/',
      data:{
        input_word :$('#search_room_input').val(),
        category:$('.narrowed_down_menu').val(),
      },
      success:function(response){
        $('.room_card').remove()
        var relation_attr = response.user_joining

        for(var key in response.hit_room_list){
          if(relation_attr.includes(response.hit_room_list[key].room_id)){
            var room_card = '<li class="room_card" role="article"><div class="room_img_detail"><a href="/room/'+response.hit_room_list[key].room_id+'/" style="display:flex; align-items:center;"><img src="/media/'+response.hit_room_list[key].room_image+'" class="room_icon"></a><div class="room_detail"><p class="room_attribution">'+response.hit_room_list[key].category+'</p><a id="room_name" href="/room/'+response.hit_room_list[key].room_id+'/">'+response.hit_room_list[key].room_name+'</a></div></div><button class="btn-change-relation '+response.hit_room_list[key].room_id+'" value='+response.hit_room_list[key].room_id+' id="secession" name="secession">退出</button></li>'
          }else{
            var room_card = '<li class="room_card" role="article"><div class="room_img_detail"><a href="/room/'+response.hit_room_list[key].room_id+'/" style="display:flex; align-items:center;"><img src="/media/'+response.hit_room_list[key].room_image+'" class="room_icon"></a><div class="room_detail"><p class="room_attribution">'+response.hit_room_list[key].category+'</p><a id="room_name" href="/room/'+response.hit_room_list[key].room_id+'/">'+response.hit_room_list[key].room_name+'</a></div></div><button class="btn-change-relation '+response.hit_room_list[key].room_id+'" value='+response.hit_room_list[key].room_id+' id="join" name="join">参加</button></li>'
          }
          $('.room_card_container').append(room_card).trigger('create');
        }
      },
      error:function(response){
      }
    })
  })

});
