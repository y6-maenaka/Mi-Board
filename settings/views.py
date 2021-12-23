from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from room.models import Rooms
from django.views.generic import ListView
from .forms import ChangeRoomInfoForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def settings_home(request):
    return render(request,'settings_home.html')

class SettingsRoomView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):

        room_list = Rooms.objects.all()

        context = {
            'room_list':room_list,
        }

        return render(request,'settings_room.html',context)

settings_room = SettingsRoomView.as_view()

class ChangeRoomNameView(LoginRequiredMixin,View):
    def get(self,request,room_id):
        room_info = Rooms.objects.filter(room_id = room_id)

        before_room_info = Rooms.objects.get(room_id = room_id)

        initial_data = {
            'room_name':before_room_info.room_name,
            'representative_person_name':before_room_info.representative_person_name,
            'room_image':before_room_info.room_image,
            'category':before_room_info.category,
            'work_time':before_room_info.work_time,
            'week_at':before_room_info.week_at,
            'subject_to':before_room_info.subject_to,

        }

        form = ChangeRoomInfoForm(
            initial=initial_data,
        )

        context = {
            'form':form,
            'room_id':room_id,
        }

        return render(request,'change_room_name.html',context)

    def post(self,request,room_id):

        modifying_data = get_object_or_404(Rooms,room_id = room_id)

        form = ChangeRoomInfoForm(request.POST, request.FILES,instance=modifying_data)
        form.save()
        return redirect('settings:settings_room')


change_room_name = ChangeRoomNameView.as_view()
