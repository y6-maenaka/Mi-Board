from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from .models import Ground
from accounts.models import Follows

class GroundGlobalView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):

        ground_list = Ground.objects.filter(ground_address='グローバル').order_by('created_at').reverse()

        context = {
            'ground_list':ground_list,
        }



        return render(request,'ground_global.html',context)

    def post(self,request,*args,**kwargs):
        return HttpResponse('')

ground_global = GroundGlobalView.as_view()


class GroundLocalView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):

        follows_list = Follows.objects.filter(followee_id=request.user.user_id).values_list('follower_id',flat=True)
        ground_list = Ground.objects.filter(post_user_id__in = follows_list,ground_address='ローカル').order_by('created_at').reverse()

        context = {
            'ground_list':ground_list,
        }

        return render(request,'ground_local.html',context)

    def post(self,request,*args,**kwargs):
        return HttpResponse('')

ground_local = GroundLocalView.as_view()

@login_required
def post_ground(request):
    if request.method == 'POST':
        ground_data = request.POST
        ground_image = request.FILES

        try:
            if ground_image['ground_image']:
                pass
        except:
            ground_image['ground_image'] = ''


        post_ground = Ground(ground_content=ground_data['ground_content'],ground_image=ground_image['ground_image'],post_user_id=request.user.user_id,ground_address=ground_data['ground_address'],post_room_id=ground_data['post_room_id'])
        post_ground.save()

        return redirect('ground:ground_global')
    return HttpResponse('')
