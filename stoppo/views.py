from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import StoppoFileStructure,ShareFile,UploadFile
import uuid
from accounts.models import Follows
import os
import json


class StoppoView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        directory_list = StoppoFileStructure.objects.filter(directory_owner_id = request.user.user_id,is_root='True').order_by('directory_name')

        upload_file_list = UploadFile.objects.filter(upload_user_id = request.user.user_id,is_root=True)
        address_list = Follows.objects.filter(followee_id = request.user.user_id)

        context = {
            'directory_list':directory_list,
            'address_list':address_list,
            'upload_file_list':upload_file_list,
        }


        return render(request,'stoppo.html',context)

    def post(self,request,*args,**kwargs):
        return HttpResponse('')

stoppo = StoppoView.as_view()

@login_required
def create_directory(request):
    if request.method == 'GET':
        new_directory_data = request.GET

        if (new_directory_data['upward_directory_id']) == str(request.user.user_id):
            new_directory = StoppoFileStructure(directory_name = new_directory_data['new_directory_name'],data_type='directory',directory_owner_id = request.user.user_id,is_root='True')

        else:
            new_directory = StoppoFileStructure(directory_name = new_directory_data['new_directory_name'],data_type='directory',directory_owner_id = request.user.user_id,upward_directory_id=new_directory_data['upward_directory_id'])

        new_directory.save()
        return HttpResponse('')

@login_required
def store_file(request):
    if request.method == 'POST':

        root,extension = os.path.splitext(str(request.FILES['upload_file']))
        try:

            upload_file = UploadFile(upload_user_id = request.user.user_id,upward_directory_id = request.POST['upward_directory_id'],file = request.FILES['upload_file'],file_name=str(request.FILES['upload_file']),extension=extension)
            upload_file.save()

        except:
            upload_file = UploadFile(upload_user_id = request.user.user_id,is_root = True,file = request.FILES['upload_file'],file_name=str(request.FILES['upload_file']),extension=extension)
            upload_file.save()

    return HttpResponse('')

@login_required
def get_directory_data(request):
    if request.method == 'GET':
        if str(request.GET['upward_directory_id']) == str(request.user.user_id):
            directory_data = StoppoFileStructure.objects.filter(directory_owner_id = request.user.user_id,is_root=True).order_by('directory_name').values()
            current_directory_file = UploadFile.objects.filter(upload_user_id = request.user.user_id,upward_directory_id=request.user.user_id).order_by('file_name').values()
        else:
            directory_data = StoppoFileStructure.objects.filter(directory_owner_id = request.user.user_id,upward_directory_id=request.GET['upward_directory_id']).order_by('directory_name').values()
            current_directory_file = UploadFile.objects.filter(upload_user_id = request.user.user_id,upward_directory_id=request.GET['upward_directory_id']).order_by('file_name').values('upload_file_id','created_at','file_name','upload_user_id','upward_directory_id','extension')

            print(current_directory_file)
        return JsonResponse({'directory_data':list(directory_data),'current_directory_file':list(current_directory_file)})


class ShareFileView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        pass

    def post(self,request,*args,**kwargs):
        pass

@login_required
def share_file(request):
    if request.method == 'GET':
        share_file_data = request.GET
        share_file = ShareFile(shared_file_id = share_file_data['share_directory_id'],receive_user_id=share_file_data['address'],send_user_id=request.user.user_id)
        share_file.save()
        return HttpResponse('')


@login_required
def share_box(request,user_id):
    shared_file_list = ShareFile.objects.filter(receive_user_id = request.user.user_id).order_by('created_at').reverse()

    context = {
        'shared_file_list':shared_file_list,
    }

    return render(request,'share_box.html',context)

@login_required
def file_view(request,file_id):
    file_data = UploadFile.objects.get(upload_file_id = file_id)
    context = {
        'file_data':file_data,
    }
    return render(request,'file_view.html',context)


@login_required
def delete_file(request,file_id):
    if request.method == 'GET':
        try:
            delete_file = UploadFile.objects.get(upload_file_id = file_id)
            delete_file.delete()

        except:
            delete_file = StoppoFileStructure.objects.get(directory = file_id)
            delete_file.delete()
    return HttpResponse('')

@login_required
def change_file_name(request,file_id):
    if request.method == 'GET':

        try:
            new_file_name = UploadFile.objects.get(upload_file_id = file_id)
            new_file_name.file_name = request.GET['new_file_name']
            new_file_name.save()
        except:
            new_file_name = StoppoFileStructure.objects.get(directory = file_id)
            new_file_name.directory_name = request.GET['new_file_name']
            new_file_name.save()
    return HttpResponse('')

@login_required
def get_file_name(request,file_id):
    if request.method == 'GET':
        try:
            file_name = UploadFile.objects.get(upload_file_id = file_id).file_name

        except:
            file_name = StoppoFileStructure.objects.get(directory = file_id).directory_name

        return JsonResponse({'file_name':file_name})
