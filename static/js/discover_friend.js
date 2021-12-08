$(function(){
  $(document).on('click','.btn-change-relation',function(){
    var state = $(this).attr('id');
    var friend_id = $(this).val();
    $.ajax({
      type : 'GET',
      url : '/discover/change_relation_friend',
      data : {
        state:state,
        friend_id:friend_id,
      },

      success:function(response){
        if(state == 'unfollow'){
          $('.'+friend_id).attr('id','follow');
          $('.'+friend_id).html('フォロー');
        }else{
          $('.'+friend_id).attr('id','unfollow');
          $('.'+friend_id).html('フォロー解除');
        }
      },
      error:function(response){
        console.log('error occured');
      }
    })
  })


  $(document).on('input','#search_friend_input',function(e){
    $.ajax({
      type:'GET',
      url:'/discover/search_friend/',
      data:{
        input_word:$('#search_friend_input').val(),
        conditions:$('.narrowed_down_menu').val()
      },
      success:function(response){
        $('.friend_card').remove()
        var relation_attr = response.user_relation
        for(var key in response.hit_friend_list){
          if(relation_attr.includes(response.hit_friend_list[key].user_id)){
            var searched_user_card = '<li class="friend_card" role="article"><div class="friend_img_detail"><a href="#" style="display:flex; align-items:center;"><img src="/media/'+response.hit_friend_list[key].user_icon_image+'" class="friend_icon"></a><div class="friend_detail"><p class="user_attribution">'+response.hit_friend_list[key].university+'|'+response.hit_friend_list[key].department+'</p><a href="#" id="friend_name">'+response.hit_friend_list[key].last_name+''+response.hit_friend_list[key].first_name+'</a></div></div><button class="btn-change-relation '+response.hit_friend_list[key].user_id+'" value='+response.hit_friend_list[key].user_id+' id="unfollow" name="unfollow"">フォロー解除</button></li>'

          }else{
          var searched_user_card = '<li class="friend_card" role="article"><div class="friend_img_detail"><a href="#" style="display:flex; align-items:center;"><img src="/media/'+response.hit_friend_list[key].user_icon_image+'" class="friend_icon"></a><div class="friend_detail"><p class="user_attribution">'+response.hit_friend_list[key].university+'|'+response.hit_friend_list[key].department+'</p><a href="#" id="friend_name">'+response.hit_friend_list[key].last_name+''+response.hit_friend_list[key].first_name+'</a></div></div><button class="btn-change-relation '+response.hit_friend_list[key].user_id+'" value='+response.hit_friend_list[key].user_id+' id="follow" name="follow"">フォロー</button></li>'
          }
        $('.friend_card_container').append(searched_user_card).trigger('create');
        }
      },
      error:function(response){
        console.log('error')
      }
    })
  })

});
