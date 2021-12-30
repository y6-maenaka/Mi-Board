from django.shortcuts import render,redirect
from django.views import View
from accounts.models import Users, Follows
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from room.models import Rooms,RoomJoining,RoomMessage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import re
from mypage.models import TimeTable
from django.db import connection
from recommend_system import views as recommend_system
from board.models import Boards

from django.core import serializers
import json

# Create your views here.

class MypageView(LoginRequiredMixin,View):
    # * args contains query parameters
    def get(self,request,*args,**kwargs):

        # timetable = TimeTable.objects.filter(user_id = request.user.user_id)

        timetable = TimeTable.objects.filter(user_id = request.user.user_id)
        timetable_data = list(timetable.values('user_id','room_id','spot'))
        for index,element in enumerate(timetable):
            timetable_data[index]['room_id'] = str(timetable_data[index]['room_id'])
            timetable_data[index]['user_id'] = str(timetable_data[index]['user_id'])
            timetable_data[index]['room_name'] = str(element.room.room_name)
            timetable_data[index]['room_image'] = str(element.room.room_image)


        '''レコメンドボード情報取得'''
        try:
            base_user = request.user.user_id
            random_extracting_user = Users.objects.filter(university = request.user.university).exclude(user_id=request.user.user_id).order_by('?')[:30].values_list('user_id',flat=True)
            # recommend_board_list = recommend_system.get_recommend_board_sub(base_user,random_extracting_user)[0:12]
            recommend_board_list = Boards.objects.all()[:4].values()
        except:
            recommend_board_list = ''
        # values : キーと値
        # values_list : 値のみ
        my_followee = Follows.objects.filter(followee_id = request.user.user_id).values_list('follower_id',flat=True)
        friend_list = Users.objects.filter(user_id__in = list(my_followee)).values('user_id','first_name','last_name','university','department','user_icon_image')


        my_joining_room = RoomJoining.objects.filter(user_id = request.user.user_id).values_list('room_id',flat=True)
        room_list = list(Rooms.objects.filter(room_id__in =my_joining_room).values('room_id','room_name','room_image'))[0:8]


        unread_room_list = []
        for _ in timetable_data:
            last_update = Rooms.objects.get(room_id = _['room_id'])
            try:
                last_access = RoomJoining.objects.get(room_id = _['room_id'],user_id = request.user.user_id)

                tmp = last_access.last_access - last_update.last_update
                if (tmp.total_seconds() < 0):
                    unread_room_list.append(_['room_id'])

            except:
                pass

        context = {
            'friend_list' : friend_list,
            'room_list':room_list,
            'recommend_board_list':recommend_board_list,
            'timetable':list(timetable_data),
            'unread_room_list':unread_room_list,
        }

        return render(request,'mypage.html',context)


    def post(self,request,*args,**kwargs):
        pass

mypage = MypageView.as_view()

@login_required
def set_room(request):
    if request.method == 'GET':


        joining_room = list(RoomJoining.objects.filter(user_id = request.user.user_id).values_list('room_id',flat=True))

        spot_num = request.GET.get('spot_num')
        """曜日と時間を抽出する"""
        mod_date = re.search('\D曜日',spot_num)
        mod_time = re.search('\d+',spot_num)

        '''曜日と時間が一致したルームを検索する'''
        match_room_list = Rooms.objects.filter(category='講義',university=request.user.university,work_time = mod_time.group(),week_at = mod_date.group()).values('room_name','room_id','room_image','university','subject_to')

        '''マッチしたルームのIDを抽出する'''
        match_room_id_list = [_['room_id'] for _ in match_room_list]

        '''ユーザの学部に一致したルームを検索する'''
        recomend_room_list = Rooms.objects.filter(category='講義',subject_to = request.user.department,university=request.user.university).exclude(room_id__in = match_room_id_list).order_by('created_at').values('room_name','room_id','room_image','university','subject_to')

        to_set_room_list = {'match_room_list':list(match_room_list),'recomend_room_list':list(recomend_room_list)}


        return JsonResponse(to_set_room_list)

@login_required
def search_set_room(request):
    if request.method == 'GET':
        input_word = request.GET.get('input_word')


        hit_room_list = Rooms.objects.filter(category='講義',university=request.user.university,room_name__istartswith=input_word).values('room_name','room_id','room_image','university','subject_to')

        return JsonResponse({'hit_room_list':list(hit_room_list)})
    return HttpResponse('')


@login_required
def add_room_timetable(request,room_id,**kwargs):
    spot_num = request.GET.get('spot')

    mod_datetime = re.search('\D曜日-\d',spot_num)

    check_timetable_exists = TimeTable.objects.filter(spot=mod_datetime.group(),user_id=request.user.user_id).values()

    #既に時間割が登録されていた場合の処理
    if check_timetable_exists.exists():
        update_room_to_timetable = TimeTable.objects.get(spot=mod_datetime.group(),user_id=request.user.user_id)
        update_room_to_timetable.room_id = room_id
        update_room_to_timetable.save()

    #新規に時間割を追加する処理
    else:
        add_room_to_timetable = TimeTable(spot=mod_datetime.group(),user_id=request.user.user_id,room_id=room_id)
        add_room_to_timetable.save()

    joining_room = RoomJoining.objects.filter(user_id = request.user.user_id).values()
    joining_room_list =  [str(_['room_id']) for _ in joining_room]

    if not room_id in joining_room_list:
        change_relation = RoomJoining(user_id = request.user.user_id,room_id = room_id)
        change_relation.save()
    return redirect('mypage:mypage',request.user.user_id)


@login_required
def get_timetable(request):
    if request.method == 'GET':
        """user_idから[-]を除去して生クエリ埋め込みに対応させる文字列に変換する"""
        user_id = str(request.user.user_id)
        user_id = user_id.replace('-','')
        user_id = f"'{user_id}'"

        #カーソルの取得
        cursor = connection.cursor()
        #生クエリ　インナージョインでスポットとルーム情報を取得
        cursor.execute(f"SELECT Rooms.room_id,Rooms.room_image,Rooms.room_name,TimeTable.spot FROM Rooms INNER JOIN TimeTable ON TimeTable.user_id={user_id} AND Rooms.room_id = TimeTable.room_id")
        user_seted_room_list = cursor.fetchall()
        return JsonResponse({'user_seted_room_list':user_seted_room_list})

@login_required
def remove_seted_room(request):
    spot_num = request.GET.get('spot')
    try:
        mod_datetime = re.search('\D曜日-\d',spot_num)
        remove_room = TimeTable.objects.get(user_id = request.user.user_id,spot = mod_datetime.group())
        remove_room.delete()

    except:
        pass
    return redirect('mypage:mypage',request.user.user_id)
