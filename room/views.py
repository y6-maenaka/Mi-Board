from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Rooms,RoomJoining,RoomMessage
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.db import connection
from accounts.models import Users
from board.models import Boards
# Create your views here.

@login_required
def room_home(request):

    room_list = RoomJoining.objects.filter(user_id = request.user.user_id)

    context = {
        'room_list':room_list,
    }
    return render(request,'room_home.html',context)

class RoomView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        room_data = Rooms.objects.get(room_id = self.kwargs['room_id'])
        room_joining = RoomJoining.objects.filter(user_id = request.user.user_id).values_list('room_id',flat=True)

        room_joining_user_list = RoomJoining.objects.filter(room_id = self.kwargs['room_id']).exclude(user_id = request.user.user_id)

        related_board_list = Boards.objects.filter(related_room_id = self.kwargs['room_id']).order_by('created_at').reverse()

        context = {
            'room_data':room_data,
            'room_joining':list(room_joining),
            'room_joining_user_list':list(room_joining_user_list),
            'num_joining_user':len(room_joining_user_list),
            'related_board_list':related_board_list,
        }

        return render(request,'room.html',context)

    def post(self,request,*args,**kwargs):
        return HttpResponse('here')

room = RoomView.as_view()

@login_required
def create_room(request):
    try:
        if request.method == 'POST':
            new_room_data = request.POST
            new_room_data_image = request.FILES

            try:
                if new_room_data_image['room_image']:
                    pass

            except:
                new_room_data_image['room_image'] = ''

            create_room_data = Rooms(room_name=new_room_data['room_name'],
                                    representative_person_name=new_room_data['representative_person_name'],
                                        category=new_room_data['category'],
                                        work_time=new_room_data['work_time'],
                                        subject_to=new_room_data['subject_to'],
                                        room_image=new_room_data_image['room_image'],
                                        week_at=new_room_data['week_at'],
                                        university=request.user.university)
            create_room_data.save()

    except:
        return redirect('room:room_home')

    return redirect('room:room_home')

class EditRoomView(LoginRequiredMixin,CreateView):
    model = Rooms
    fields = ['room_name']

edit_room = EditRoomView.as_view()

@login_required
def get_message(request,room_id):
    if request.method == 'GET':
        room_id = request.GET.get('room_id')
        message_list = RoomMessage.objects.filter(room_id = room_id).values('message','send_user_id')
        return JsonResponse({'message_list':list(message_list)})
