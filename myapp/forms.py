from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Talk
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)

from allauth.account.forms import ( 
    LoginForm, 
    SignupForm, 
    ResetPasswordKeyForm, 
    ResetPasswordForm
)

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "img",)
class LoginForm(AuthenticationForm):
    pass
class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ("talk",)
        # 入力予測の表示をさせない（めっちゃ邪魔）
        widgets = {"talk": forms.TextInput(attrs={"autocomplete": "off"})}
class ImageSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("img",)
class MailSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {"email": "新しいメールアドレス"}

class UserNameSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "新しい名前"}

class PasswordChangeForm(PasswordChangeForm):
    pass

class FriendsSearchForm(forms.Form):
    """友達の中から任意のユーザーを検索"""

    keyword = forms.CharField(
        label="検索",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "ユーザー名で検索",
            "autocomplete": "off",
            }
        ),
    )

class MySignupForm(SignupForm):
    """ Userクラス用フォーム """
    img = forms.ImageField()
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # プレースホルダー(フォームの中に入れるガイドの文字)を設定できる
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード(確認用)'

        # for で回して各フォームに設定を追加できる
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"
            if field != self.fields['img']:
                field.widget.attrs['class'] = 'form-control'
    
    def signup(self, request, user):
        user.img = self.cleaned_data['img']
        user.save()
        return user
