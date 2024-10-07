from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Talk
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
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

