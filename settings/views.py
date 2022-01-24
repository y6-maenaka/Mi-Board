from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from room.models import Rooms
from django.views.generic import ListView
from .forms import ChangeRoomInfoForm
from django.contrib.auth.decorators import login_required
from .models import Report
from accounts.models import Users,PointsHistory
from django.http import HttpResponse,JsonResponse
from stoppo.models import UploadFile

# Create your views here.

@login_required
def settings_home(request):
    if request.user.authority == 'general':
        return HttpResponse(status=500)
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
def stoppo_settings(request):
    if request.method == 'GET':
        if request.user.authority == 'general':
            return HttpResponse(status=500)
        all_upload_file = UploadFile.objects.all().order_by('created_at').reverse()
        all_upload_file_size = 0
        for file in all_upload_file:
            if file.file_size == None:
                pass
            else:
                all_upload_file_size += int(file.file_size)


        context = {
            'all_upload_file':all_upload_file,
            'all_upload_file_size':all_upload_file_size/1000000000,
        }
        return render(request,'stoppo_settings.html',context)

@login_required
def list_report(request):
    if request.method == 'GET':
        if request.user.authority == 'general':
            return HttpResponse(status=500)
        list_report = Report.objects.all().order_by('created_at').reverse()
        context = {
            'list_report':list_report,
        }
        return render(request,'list_report.html',context)

@login_required
def list_user_info(request):
    if request.method == 'GET':
        if request.user.authority == 'general':
            return HttpResponse(status=500)
        list_user_info = Users.objects.all().exclude(user_id = request.user.user_id).order_by('created_at')
        context = {
            'list_user_info':list_user_info,
        }
        return render(request,'list_user_info.html',context)

@login_required
def points_history(request):
    if request.method == 'GET':
        points_history = PointsHistory.objects.filter(consumed_user_id=request.user.user_id).order_by('created_at').reverse()
        context = {
            'points_history':points_history,
        }
        return render(request,'points_history.html',context)

class SettingsRoomView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        if request.user.authority == 'general':
            return HttpResponse(status=500)

        room_list = Rooms.objects.all()

        context = {
            'room_list':room_list,
        }

        return render(request,'settings_room.html',context)

settings_room = SettingsRoomView.as_view()

class ChangeRoomNameView(LoginRequiredMixin,View):
    def get(self,request,room_id):
        if request.user.authority == 'general':
            return HttpResponse(status=500)
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
        if request.user.authority == 'general':
            return HttpResponse(status=500)

        modifying_data = get_object_or_404(Rooms,room_id = room_id)

        form = ChangeRoomInfoForm(request.POST, request.FILES,instance=modifying_data)
        form.save()
        return redirect('settings:settings_room')


change_room_name = ChangeRoomNameView.as_view()
