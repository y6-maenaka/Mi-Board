from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from accounts.models import Users
from django.utils import timezone
# Create your views here.

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
        return render(request,'about_mi_Board.html',context)

about_mi_board = AboutMiBoardView.as_view()


def ranking(request):
    if request.method == 'GET':

        spend_days = timezone.now() - request.user.created_at
        ranking_regist = Users.objects.all().order_by('created_at')[:7]

        ranking_points = Users.objects.all().order_by('points').reverse()[:7]

        context = {
            'spend_days': spend_days.days,
            'ranking_regist':ranking_regist,
            'ranking_points':ranking_points,
        }
        return render(request,'ranking.html',context)
