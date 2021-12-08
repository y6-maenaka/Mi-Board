// $(function(){
//   var url = location.pathname
//   window.onload = function(){
//     $.ajax({
//       type:'GET',
//       url:"/friend/get_friend_timetable/?friend_id="+url+"",
//       success:function(response){
//         for(var key in response.friend_timetable_list){
//           var timetable_room_card = '<div class="spot_container"><a href="#" class="link_container_room_image" href="/room/'+response.friend_timetable_list[key][0]+'/"><img src="/media/'+response.friend_timetable_list[key][1]+'" class="timetable_room_icon"></a><a class="link_container_room_name" href="/room/'+response.friend_timetable_list[key][0]+'/">'+response.friend_timetable_list[key][2]+'</a></div>'
//           $("#"+response.friend_timetable_list[key][3]).append(timetable_room_card)
//         }
//       },
//       error:function(response){
//         console.log('error')
//       }
//     })
//   }
// })
