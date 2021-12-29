from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from room.models import Rooms
from django.views.generic import ListView
from .forms import ChangeRoomInfoForm
from django.contrib.auth.decorators import login_required
from .models import Report
from accounts.models import Users

# Create your views here.

@login_required
def settings_home(request):
    return render(request,'settings_home.html')

class SendReportView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        return render(request,'send_report.html')

    def post(self,request,*args,**kwargs):
        report = request.POST
        store_report = Report(user_id=request.user.user_id,report=report['report'])
        store_report.save()

        context = {
            'complete_send_report':'complete_send_report',
        }

        return render(request,'send_report.html',context)

send_report = SendReportView.as_view()

@login_required
def list_report(request):
    if request.method == 'GET':
        list_report = Report.objects.all().order_by('created_at').reverse()
        context = {
            'list_report':list_report,
        }
        return render(request,'list_report.html',context)

@login_required
def list_user_info(request):
    if request.method == 'GET':
        list_user_info = Users.objects.all().exclude(user_id = request.user.user_id).order_by('created_at')
        context = {
            'list_user_info':list_user_info,
        }
        return render(request,'list_user_info.html',context)

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


class AboutMiBoardView(View):
    def get(self,request,*args,**kwargs):
        user_list = list(Users.objects.all().values_list('department',flat=True))
        context = {
            'engineering':int(user_list.count('工学部')),
            'agriculture':int(user_list.count('農学部')),
            'education':int(user_list.count('教育学部')),
            'region':int(user_list.count('地域資源創生学部')),
            'medicine':int(user_list.count('医学部')),
            'total':int(len(user_list)),
        }
        return render(request,'about_mi_board.html',context)

about_mi_board = AboutMiBoardView.as_view()
