from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from accounts.models import Follows,PersonalChatLayerGroup
from django.contrib.auth.decorators import login_required
from accounts.models import Users
from personal_chat.models import Message
# Create your views here.

class PersonalChatView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):

        talker_list = PersonalChatLayerGroup.objects.filter(Q(owner_user_id=request.user.user_id)|Q(invited_user_id=request.user.user_id)).order_by('last_update').reverse()

        context = {
            'talker_list':talker_list,
        }


        return render(request,'personal_chat.html',context)

    def post(self,request,*args,**kwargs):
        pass


personal_chat = PersonalChatView.as_view()


@login_required
def add_talker(request):
    """新しくチャットを開始する人を探す場合"""
    if request.method == 'GET':
        yet_talker_owner = list(PersonalChatLayerGroup.objects.filter(owner_user_id = request.user.user_id).values_list('invited_user_id',flat=True))
        yet_talker_inviter = list(PersonalChatLayerGroup.objects.filter(invited_user_id=request.user.user_id).values_list('owner_user_id',flat=True))

        """既にグループがある人を選び出す(uuidの為苦戦)"""
        yet_talker = []

        for _ in yet_talker_owner:
            yet_talker.append(str(_))
        else:
            for _ in yet_talker_inviter:
                yet_talker.append(str(_))


        #既にトーク相手が一人以上いた場合
        if yet_talker:
            new_followee_list = Follows.objects.filter(followee_id = request.user.user_id).exclude(follower_id__in = yet_talker).values_list('follower_id',flat=True)
            new_talker_list = Users.objects.filter(user_id__in = list(new_followee_list)).values('user_id','first_name','last_name','user_icon_image','university','department')
        #まだトーク相手がいない場合
        else:
            new_followee_list = Follows.objects.filter(followee_id = request.user.user_id).values_list('follower_id',flat=True)
            new_talker_list = Users.objects.filter(user_id__in = list(new_followee_list)).values('user_id','first_name','last_name','user_icon_image','university','department')

        return JsonResponse({'new_talker_list':list(new_talker_list)})


    """検索をかけたときに表示する人のリスト"""
    if request.method == 'POST':
        input_word = request.POST.get('input_word')
        if len(input_word) >= 1:
            found_talker_list = Users.objects.filter(Q(first_name__istartswith=input_word)|Q(last_name__istartswith=input_word)).exclude(user_id=request.user.user_id).values('user_id','first_name','last_name','user_icon_image','university','department')
            return JsonResponse({'found_talker_list':list(found_talker_list)})
        else:
            pass
    return HttpResponse('here is add_talker view')


'''新規に宛先を登録する'''
@login_required
def register_talker(request,friend_id):
    if request.method == 'GET':
        register_talker = PersonalChatLayerGroup(owner_user_id = request.user.user_id,invited_user_id=friend_id)
        register_talker.save()

    return redirect('personal_chat:personal_chat')

@login_required
def get_message(request,friend_id):
    if request.method == 'GET':
        talker_id = request.GET.get('talker_id')
        talker_data = Users.objects.filter(user_id=talker_id).values('first_name','last_name','user_icon_image','user_id')
        #message_tableが大きくなるのでjoinでは遅くなる
        group_name = PersonalChatLayerGroup.objects.get(Q(invited_user_id=talker_id,owner_user_id=request.user.user_id)|Q(invited_user_id=request.user.user_id,owner_user_id=talker_id))
        message_list = Message.objects.filter(group_name_id=group_name).values('message','send_by','send_user_id')

    return JsonResponse({'message_list':list(message_list),'talker_data':list(talker_data)})
