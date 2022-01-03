from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from accounts.models import Users

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
        return render(request,'about_mi_board.html',context)

about_mi_board = AboutMiBoardView.as_view()
