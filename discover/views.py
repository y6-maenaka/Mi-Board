from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,JsonResponse
from accounts.models import Users,Follows
from room.models import Rooms,RoomJoining
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core import serializers

class DiscoverFriendView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        accounts_list = Users.objects.all().exclude(user_id=request.user.user_id).values(
            'user_id',
            'university',
            'first_name',
            'last_name',
            'department',
            'division',
            'user_icon_image',
        )

        follows = Follows.objects.filter(followee_id = request.user.user_id).values_list('follower_id',flat=True)


        context = {
            'accounts_list' : list(accounts_list),
            'follows' : list(follows),
        }

        return render(request,'discover_friend.html',context)

    def post(self,request,*args,**kwargs):
        pass

discover_friend = DiscoverFriendView.as_view()

class DiscoverRoomView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        room_list = Rooms.objects.all().values(
            'room_id',
            'room_name',
            'category',
            'room_image',
        )



        joining = RoomJoining.objects.filter(user_id = request.user.user_id).values_list('room_id',flat=True)

        context = {
            'room_list': list(room_list),
            'joining' : joining,
        }

        return render(request,'discover_room.html',context)


    def post(self,request,*args,**kwargs):
        pass

discover_room = DiscoverRoomView.as_view()

@login_required
def change_relation_friend(request):
    if request.GET['state'] == 'follow':
        change_relation = Follows(followee_id = request.user.user_id,follower_id = request.GET['friend_id'])
        change_relation.save()

    elif request.GET['state'] == 'unfollow':
        change_relation = Follows.objects.filter(followee_id = request.user.user_id,follower_id = request.GET['friend_id'])
        change_relation.delete()

    else:
        pass
    return HttpResponse('')


@login_required
def change_relation_room(request):
    if request.GET['state'] == 'join':
        change_relation = RoomJoining(user_id = request.user.user_id, room_id = request.GET['room_id'])
        change_relation.save()

    elif request.GET['state'] == 'secession':
        change_relation = RoomJoining.objects.filter(user_id = request.user.user_id, room_id = request.GET['room_id'])
        change_relation.delete()

    else:
        print('error')

    return HttpResponse('here is change_relaton_room view')

@login_required
def search_friend(request):
    if request.method == 'GET':

        input_word = request.GET.get('input_word')
        conditions = request.GET.get('conditions')

        user_relation = Follows.objects.filter(followee_id = request.user.user_id).values_list('follower_id',flat=True)

        if conditions == 'university':
            hit_friend_list = Users.objects.filter(university__istartswith = input_word).exclude(user_id = request.user.user_id).values()
            return JsonResponse({'hit_friend_list':list(hit_friend_list),"user_relation":list(user_relation)})

        if conditions == 'department':
            hit_friend_list = Users.objects.filter(department__istartswith = input_word).exclude(user_id = request.user.user_id).values()
            return JsonResponse({'hit_friend_list':list(hit_friend_list),"user_relation":list(user_relation)})

        if conditions == 'circle':
            hit_friend_list = Users.objects.filter(circle__istartswith = input_word).exclude(user_id = request.user.user_id).values()
            return JsonResponse({'hit_friend_list':list(hit_friend_list),"user_relation":list(user_relation)})

        if conditions == 'part_time_job':
            hit_friend_list = Users.objects.filter(part_time_job__istartswith = input_word).exclude(user_id = request.user.user_id).values()
            return JsonResponse({'hit_friend_list':list(hit_friend_list),"user_relation":list(user_relation)})

        if conditions == 'hometown':
            hit_friend_list = Users.objects.filter(hometown__istartswith = input_word).exclude(user_id = request.user.user_id).values()
            return JsonResponse({'hit_friend_list':list(hit_friend_list),"user_relation":list(user_relation)})

        if conditions == 'high_school':
            hit_friend_list = Users.objects.filter(high_school__istartswith = input_word).exclude(user_id = request.user.user_id).values()
            return JsonResponse({'hit_friend_list':list(hit_friend_list),"user_relation":list(user_relation)})

        if conditions == 'user_name':
            hit_friend_list = Users.objects.filter(Q(first_name__istartswith = input_word)|Q(last_name__istartswith = input_word)).exclude(user_id = request.user.user_id).values()
            return JsonResponse({'hit_friend_list':list(hit_friend_list),"user_relation":list(user_relation)})
    return HttpResponse('')


@login_required
def search_room(request):
    if request.method == 'GET':

        input_word = request.GET.get('input_word')
        category = request.GET.get('category')


        user_joining = RoomJoining.objects.filter(user_id = request.user.user_id).values_list('room_id',flat=True)

        if category == '講義':
            hit_room_list = Rooms.objects.filter(category='講義',room_name__istartswith=input_word).values()
            return JsonResponse({'hit_room_list':list(hit_room_list),'user_joining':list(user_joining)})

        if category == 'その他':
            hit_room_list = Rooms.objects.filter(category='その他',room_name__istartswith=input_word).values()


            return JsonResponse({'hit_room_list':list(hit_room_list),'user_joining':list(user_joining)})
    return HttpResponse('')
