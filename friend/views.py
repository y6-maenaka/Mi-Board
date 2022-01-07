from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponse, JsonResponse
from accounts.models import Users,Follows
from django.contrib.auth.decorators import login_required
import re
from accounts.models import Follows
from mypage.models import TimeTable
# Create your views here.

@login_required
def friend_home(request):
    followee_list = Follows.objects.filter(followee_id = request.user.user_id)

    follower_list = Follows.objects.filter(follower_id = request.user.user_id)


    context = {
        'followee_list':followee_list,
        'follower_list':follower_list,
    }

    return render(request,'friend_home.html',context)

class FriendProfileView(LoginRequiredMixin,View):
    # * args contains query parameters
    def get(self,request,*args,**kwargs):

        friend_id = self.kwargs['friend_id']

        if str(friend_id) == str(request.user.user_id):
            return redirect('friend:friend_home')

        """フレンドプロフィールデータ取得"""
        friend_profile_data = Users.objects.values(
                                        'user_id',
                                        'university',
                                        'last_name',
                                        'first_name',
                                        'department',
                                        'division',
                                        'laboratory',
                                        'part_time_job',
                                        'circle',
                                        'hometown',
                                        'high_school',
                                        'detail',
                                        'user_icon_image',
                                        'user_background_image',
                                        'sns_link_twitter',
                                        'sns_link_instagram',
                                        'sns_link_facebook',
                                        ).get(user_id = self.kwargs['friend_id'])

        friend_profile_data = {key : value for key, value in friend_profile_data.items() if value is not None}

        #css用ルートパスに変換
        try:
            add_background_image_path = f'/media/{friend_profile_data["user_background_image"]}'
            friend_profile_data['user_background_image'] = add_background_image_path

        except:
            pass

        follows = Follows.objects.filter(followee_id = request.user.user_id,follower_id = friend_id)



        friend_followee = Follows.objects.filter(followee_id = friend_id).values_list('follower_id',flat=True)
        friend_friend_list = Users.objects.filter(user_id__in = friend_followee).values('user_id','first_name','last_name','user_icon_image','department','university')



        friend_follower_id_list = Follows.objects.filter(followee_id = self.kwargs['friend_id']).values_list('follower_id',flat=True)
        if not request.user.user_id in friend_follower_id_list:
            timetable_data = ''

        else:
            timetable = TimeTable.objects.filter(user_id = self.kwargs['friend_id'])
            timetable_data = list(timetable.values('user_id','room_id','spot'))
            for index,element in enumerate(timetable):
                timetable_data[index]['room_id'] = str(timetable_data[index]['room_id'])
                timetable_data[index]['user_id'] = str(timetable_data[index]['user_id'])
                timetable_data[index]['room_name'] = str(element.room.room_name)
                timetable_data[index]['room_image'] = str(element.room.room_image)


        context = {
            'friend_profile_data' : friend_profile_data,
            'friend_friend_list': friend_friend_list,
            'timetable':list(timetable_data),
            'follows':follows,
        }

        return render(request,'friend_profile.html',context)

    def post(self,request,*args,**kwargs):
        pass

friend_profile = FriendProfileView.as_view()
#
# @login_required
# def get_friend_timetable(request):
#     if request.method == 'GET':
#         accessing_url = request.GET.get('friend_id')
#
#         """URLからmysqlで使う形に成形"""
#         extracted_friend_id = (re.search('/\S{36}/',accessing_url)).group()
#         replace_1_friend_id = extracted_friend_id.replace('/','')
#         mod_friend_id = replace_1_friend_id.replace('-','')
#         friend_id = f"'{mod_friend_id}'"
#
#         friend_follower_id_list = Follows.objects.filter(followee_id = replace_1_friend_id).values_list('follower_id',flat=True)
#         if not request.user.user_id in friend_follower_id_list:
#             friend_timetable_list = ''
#
#         else:
#             cursor = connection.cursor()
#             cursor.execute(f"SELECT Rooms.room_id,Rooms.room_image,Rooms.room_name,TimeTable.spot FROM Rooms INNER JOIN TimeTable ON TimeTable.user_id={friend_id} AND Rooms.room_id = TimeTable.room_id")
#             friend_timetable_list = cursor.fetchall()
#         return JsonResponse({'friend_timetable_list':friend_timetable_list})
