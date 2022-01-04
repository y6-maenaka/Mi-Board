from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.http import HttpResponse
from .models import Users
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, ProfileEditForm
from board.models import Boards,GoodBoard,StoreBoard
from ground.models import Ground
from django.views import generic
from django.template.loader import render_to_string
from django.http import Http404, HttpResponseBadRequest
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.core.mail import send_mail
# Create your views here.


User = get_user_model()

class RegisterView(View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('mypage:mypage',request.user.user_id)

        context = {
            'form': RegisterForm(),
        }
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        print('here')

        # リクエストからフォームを作成
        form = RegisterForm(request.POST,request.FILES)
        # バリデーション
        if not form.is_valid():
            print('before')
            # バリデーションNGの場合はアカウント登録画面のテンプレートを再表示
            return render(request, 'register.html', {'form': form})


        # 保存する前に一旦取り出す
        user = form.save(commit=False)
        # パスワードをハッシュ化してセット
        user.set_password(form.cleaned_data['password'])
        user.is_active = False
        # ユーザーオブジェクトを保存
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain

        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(str(user.pk)),
            'user': user,
        }

        #txtファイルを使う為の設定(render_to_string)

        subject = render_to_string('mail_template/subject.txt', context)
        message = render_to_string('mail_template/message.txt', context)


        recipient_list = []
        recipient_list.append(user.email)

        send_mail(subject,message,'Mi-Board',recipient_list)
        return redirect('accounts:user_create_done')

        #  ログイン処理（取得した Userオブジェクトをセッションに保存 & Userデータを更新）
        # auth_login(request, user)
        #
        # return redirect('mypage:mypage',user_id=request.user.user_id)

class UserCreateDone(generic.TemplateView):
    template_name = 'user_create_done.html'

class UserCreateComplete(generic.TemplateView):
    template_name = 'user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)

    def get(self,request,**kwargs):
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = Users.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

register = RegisterView.as_view()


class LoginView(View):
    def get(self, request, *args, **kwargs):
        """GETリクエスト用のメソッド"""
        print('user state is',request.user.is_authenticated)
        if request.user.is_authenticated:

            return redirect('mypage:mypage',request.user.user_id)

        context = {
            'form': LoginForm(),
        }
        # ログイン画面用のテンプレートに値が空のフォームをレンダリング
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        """POSTリクエスト用のメソッド"""
        # リクエストからフォームを作成
        form = LoginForm(request.POST)
        # バリデーション（ユーザーの認証も合わせて実施）
        if not form.is_valid():
            # バリデーションNGの場合はログイン画面のテンプレートを再表示
            return render(request, 'login.html', {'form': form})

        # ユーザーオブジェクトをフォームから取得
        user = form.get_user()

        # ログイン処理（取得したユーザーオブジェクトをセッションに保存 & ユーザーデータを更新） ユーザ登録も兼ねる
        auth_login(request, user)

        return redirect('mypage:mypage',user_id=user.user_id)


login = LoginView.as_view()


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            # ログアウト処理
            auth_logout(request)

        return redirect(reverse('accounts:login'))


logout = LogoutView.as_view()



class ProfileEditView(View):
    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect(reverse('accounts:login'))

        before_user_profile = Users.objects.get(user_id = request.user.user_id)

        initial_data = {
            'email' : before_user_profile.email,
            'last_name' : before_user_profile.last_name,
            'first_name' : before_user_profile.first_name,
            'department' : before_user_profile.department,
            'division' : before_user_profile.division,
            'laboratory' : before_user_profile.laboratory,
            'circle' : before_user_profile.circle,
            'hometown' : before_user_profile.hometown,
            'high_school' : before_user_profile.high_school,
            'detail' : before_user_profile.detail,
            'sns_link_twitter' : before_user_profile.sns_link_twitter,
            'sns_link_instagram' : before_user_profile.sns_link_instagram,
            'sns_link_facebook' : before_user_profile.sns_link_facebook,
            'user_icon_image' : before_user_profile.user_icon_image,
            'user_background_image' : before_user_profile.user_background_image,
        }

        form = ProfileEditForm(
            initial=initial_data,
        )

        context = {
            'form' : form,
        }
        return render(request,'profile_edit.html',context)

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect(reverse('accounts:login'))

        modifying_data = get_object_or_404(Users,user_id = request.user.user_id)

        form = ProfileEditForm(request.POST, request.FILES, instance=modifying_data)
        form.save()

        if not form.is_valid():
            context = {
                'form':form,
                'user_id':request.user.user_id,
            }

        return redirect('mypage:mypage',user_id = request.user.user_id)

profile_edit = ProfileEditView.as_view()


class ProfileView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        """ユーザープロフィールデータ取得"""
        user_profile_data = Users.objects.values(
                                        'university',
                                        'last_name',
                                        'first_name',
                                        'department',
                                        'division',
                                        'laboratory',
                                        'part_time_job',
                                        'circle',
                                        'hometown',
                                        'high_school',
                                        'detail',
                                        'user_icon_image',
                                        'user_background_image',
                                        'sns_link_twitter',
                                        'sns_link_instagram',
                                        'sns_link_facebook',
                                        ).get(user_id = request.user.user_id)



        user_profile_data = {key : value for key, value in user_profile_data.items() if value is not None}

        try:
            add_background_image_path = f'/media/{user_profile_data["user_background_image"]}'
            user_profile_data['user_background_image'] = add_background_image_path

        except:
            pass


        post_board_list = Boards.objects.filter(posted_by_id = request.user.user_id).values().order_by('created_at').reverse()

        good_board_id_list = GoodBoard.objects.filter(good_user_id = request.user.user_id).values_list('board_id',flat=True)
        good_board_list = Boards.objects.filter(board_id__in = good_board_id_list).values()

        store_board_id_list = StoreBoard.objects.filter(store_user_id = request.user.user_id).values_list('board_id',flat=True)
        store_board_list = Boards.objects.filter(board_id__in = store_board_id_list).values()

        # ground_list = Ground.objects.filter(post_user_id = request.user.user_id)

        context = {
            'user_profile_data':user_profile_data,
            'post_board_list':post_board_list,
            'good_board_list':good_board_list,
            'store_board_list':store_board_list,
            # 'ground_list':ground_list,
        }

        return render(request,'profile.html',context)

    def post(self,request,*args,**kwargs):
        return HttpRespons('')

profile = ProfileView.as_view()
