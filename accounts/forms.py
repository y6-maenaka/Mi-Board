from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ObjectDoesNotExist
from .models import Users


User = get_user_model()

class RegisterForm(forms.ModelForm):
    """ユーザー登録画面用のフォーム"""

    class Meta:
        model = Users


        fields = (
            'username',
            'password',
            'email',
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
            )

    university = forms.fields.ChoiceField(
        label = '学校選択',
        required = True,
        disabled = False,
        choices=[
            ('宮崎大学','宮崎大学')],
        widget = forms.Select(attrs={
                'id':'choice_university',}))

    department = forms.fields.ChoiceField(
        label = '学部選択',
        required = True,
        disabled = False,
        choices=[
            ('工学部','工学部'),
            ('教育学部','教育学部'),
            ('農学部','農学部'),
            ('医学部','医学部'),
            ('地域資源創生学部','地域資源創生学部')],
        widget = forms.Select(attrs={
                'id':'choice_department',}))

    division = forms.fields.ChoiceField(
        label = '学科選択',
        required = True,
        disabled = False,
        choices=[
            ('情報通信工学系','情報通信工学系'),
            ('応用物質科学系','応用物質科学系'),
            ('土木環境工学系','土木環境工学系'),
            ('応用物理工学系','応用物理工学系'),
            ('電気電子工学系','電気電子工学系'),
            ('機械知能工学系','機械知能工学系'),
            ('小中一貫教育コース','小中一貫教育コース'),
            ('教職実践基礎コース','教職実践基礎コース'),
            ('発達支援教育コース','発達支援教育コース'),
            ('植物生産環境学科','植物生産環境学科'),
            ('森林緑地環境科学学科','森林緑地環境科学学科'),
            ('海洋生物環境学科','海洋生物環境学科'),
            ('畜産草地科学科','畜産草地科学科'),
            ('獣医学科','獣医学科'),
            ('応用生物科学科','応用生物科学科'),
            ('医学科','医学科'),
            ('看護学科','看護学科')
            ],
        widget = forms.Select(attrs={
                'id':'choice_division',}))



    password2 = forms.CharField(
        label='ログインパスワード(確認用)',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'ログインパスワード(確認用)'}),
    )

    username = forms.CharField(
        label='ログインID',
        required=True,
        strip=False,
        widget=forms.TextInput(attrs={'placeholder': 'ログインID (例:example000'}),
    )

    password = forms.CharField(
        label='ログインパスワード',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'ログインパスワード (例:secured-0123'}),
    )

    last_name = forms.CharField(
        label='苗字',
        required=True,
        strip=False,
        widget=forms.TextInput(attrs={'placeholder': '苗字'}),
    )

    first_name = forms.CharField(
        label='苗字',
        required=True,
        strip=False,
        widget=forms.TextInput(attrs={'placeholder': '名前'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # フィールドの属性を書き換え
        self.fields['email'].widget.attrs = {'placeholder': 'メールアドレス'}
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def claen_username(self):
        value = self.cleaned_data['username']
        if len(value) <= 5:
            raise forms.ValidationError(
                '6文字以上20文字以内で入力して下さい',
                params = {'min_length': 6 }
            )
        return value

    def clean_password(self):
        value = self.cleaned_data['password']
        return value

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        if not 'student.miyazaki-u.ac.jp' in email:
            raise forms.ValidationError('学生用メールアドレスを入力してください。')
        return email

    def clead(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise forms.ValidationError('パスワードと確認用パスワードが合致しません')

        super().clean()



class LoginForm(forms.Form):
    """ログイン画面用のフォーム"""

    username = UsernameField(
        label='ユーザー名',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'ユーザー名', 'autofocus': True}),
    )

    password = forms.CharField(
        label='パスワード',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}, render_value=True),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean_password(self):
        value = self.cleaned_data['password']
        return value

    def clean_username(self):
        value = self.cleaned_data['username']
        # if len(value) < 6:
        #     raise forms.ValidationError(
        #         '%(min_length)s文字以上で入力してください', params={'min_length': 6})
        return value

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError("正しいユーザー名を入力してください")
        # パスワードはハッシュ化されて保存されているので平文での検索はできない
        if not user.check_password(password):
            raise forms.ValidationError("正しいユーザー名とパスワードを入力してください")
        # 取得したユーザーオブジェクトを使い回せるように内部に保持しておく
        self.user_cache = user

    def get_user(self):
        return self.user_cache



class ProfileEditForm(forms.ModelForm):

    user_icon_image = forms.ImageField(widget=forms.FileInput)
    user_background_image = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = Users
        fields = (
            #自動登録
            # 'university',
            'last_name',
            'first_name',
            'laboratory',
            'part_time_job',
            'circle',
            'hometown',
            'high_school',
            'detail',
            'sns_link_twitter',
            'sns_link_instagram',
            'sns_link_facebook',
            'user_icon_image',
            'user_background_image',
        )



    def clean_first_name(self):
        value = self.cleaned_data['first_name']
        if len(value) >= 9:
            raise forms.ValidationError(
                '8文字以内で入力してください'
            )
        return value

    def clean_last_name(self):
        value = self.cleaned_data['last_name']
        if len(value) >= 9:
            raise forms.validationError(
                '8文字以内で入力してください'
            )
        return value


    def clean_laboratory(self):
        if self.cleaned_data['laboratory']:
            value = self.cleaned_data['laboratory']
            if len(value) >= 11:
                raise forms.ValidationError(
                    '10文字以内で入力してしてください'
                )
            return value

    def clean_part_time_job(self):
        if self.cleaned_data['part_time_job']:
            value = self.cleaned_data['part_time_job']
            if len(value) >= 9:
                raise forms.ValidationError(
                    '8文字以内で入力してしてください'
                )
            return value

    def clean_circle(self):
        if self.cleaned_data['circle']:
            value = self.cleaned_data['circle']
            if len(value) >= 9:
                raise forms.ValidationError(
                    '8文字以内で入力してしてください'
                )
            return value

    def clean_hometown(self):
        if self.cleaned_data['hometown']:
            value = self.cleaned_data['hometown']
            if len(value) >= 11:
                raise forms.ValidationError(
                    '10文字以内で入力してしてください'
                )
            return value

    def clean_high_shcool(self):
        if self.cleaned_data['high_school']:
            value = self.cleaned_data['high_school']
            if len(value) >= 11:
                raise forms.ValidationError(
                    '10文字以内で入力してしてください'
                )
            return value

    def clean_detail(self):
        if self.cleaned_data['detail']:
            value = self.cleaned_data['detail']
            if len(value) >= 251:
                raise forms.ValidationError(
                    '250文字以内で入力してしてください'
                )
            return value

    def clean_sns_link_twitter(self):
        if self.cleaned_data['sns_link_twitter']:
            value = self.cleaned_data['sns_link_twitter']
            if len(value) >= 255:
                raise forms.ValidationError(
                    '254文字以内で入力してしてください'
                )
            return value

    def clean_sns_link_instagram(self):
        if self.cleaned_data['sns_link_instagram']:
            value = self.cleaned_data['sns_link_instagram']
            if len(value) >= 255:
                raise forms.ValidationError(
                    '254文字以内で入力してしてください'
                )
            return value

    def clean_sns_link_facebook(self):
        if self.cleaned_data['sns_link_facebook']:
            value = self.cleaned_data['sns_link_facebook']
            if len(value) >= 255:
                raise forms.ValidationError(
                    '254文字以内で入力してしてください'
                )
            return value

    def clean_user_icon_image(self):
        value = self.cleaned_data['user_icon_image']
        return value

    def clean_user_background_image(self):
        value = self.cleaned_data['user_background_image']
        return value
