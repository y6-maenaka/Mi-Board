$(function(){
  $(document).on('click','.friend_profile_follow',function(){
    var state = $(this).attr('id');
    var friend_id = $(this).val();
    $.ajax({
      type:'GET',
      url: '/discover/change_relation_friend',
      data:{
        state:state,
        friend_id:friend_id,
      },
      success:function(response){
        if(state == 'unfollow'){
          $('.friend_profile_follow').attr('id','follow');
          $('.friend_profile_follow').html('フォロー');
        }else{
          $('.friend_profile_follow').attr('id','unfollow');
          $('.friend_profile_follow').html('フォロー解除');
        }
      },
      error:function(response){
      }
    })
  })

})
