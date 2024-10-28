import operator
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.db.models import Q, F, OuterRef, Subquery, Max, Case, When
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .forms import (
    SignUpForm,
    TalkForm,
    ImageSettingForm,
    PasswordChangeForm,
    UserNameSettingForm,
    MailSettingForm,
    LoginForm,
    FriendsSearchForm,
)

from .models import CustomUser,Talk
from .utils import create_info_list 

from django.views.generic import ListView

# from .models import Talk
User = get_user_model()


def index(request):
    return render(request, "myapp/index.html")

# def signup_view(request):
#     if request.POST:
#         #送信情報をフォームに渡す。(実際はUserCreationFormを継承した自作のモデルフォームを使うことになります。)
#         form = UserCreationForm(request.POST,request.FILES)
#         print(request.POST)
#         print(request.FILES)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password1")
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#             return redirect('')
#     else:
#         form = UserCreationForm()
#     return render(request, "myapp/signup.html")

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        error_message = ''
    elif request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        # print(form.fields)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("/")
        else:
            print(form.errors)

    context = {
            "form": form,
        }
    return render(request, "myapp/signup.html", context)

class Login(LoginView):
    template_name = 'myapp/login.html'
    success_url = reverse_lazy('frieds')
    authentication_form = LoginForm

# def friends(request):
#     return render(request, "myapp/friends.html")

class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""

"""
@login_required
def friends(request):
    user = request.user
    friends = User.objects.exclude(id=user.id).prefetch_related("talk_to", "talk_from")

    #create_info_list()関数は、ログインしているユーザーを表すuserとuser以外のアカウント全体のquerysetを表すfriendsを入力として、userのトーク内容で更新が最新のものが先頭に近くなった多次元リストを作成する。
    info = create_info_list(user, friends)
    
    # 検索機能
    form = FriendsSearchForm()
    if request.method == "GET" and "friends_search" in request.GET:
        form = FriendsSearchForm(request.GET)


        # 送信内容があった場合
        if form.is_valid():
            keyword = form.cleaned_data.get("keyword")
            email_keyword = form.cleaned_data.get("email")
            if keyword:
                friends = friends.filter(username__icontains=keyword)
                info = create_info_list(user, friends)
                context = {
                    "info": info,
                    "form": form,
                    # 検索結果を表示していることを示すためのブーリアン
                    "is_searched": True,
                }
                return render(request, "myapp/friends.html", context)
            
            if email_keyword:
                friends = friends.filter(email__icontains=email_keyword)
                info = create_info_list(user, friends)
                context = {
                    "info": info,
                    "form": form,
                    # 検索結果を表示していることを示すためのブーリアン
                    "is_searched": True,
                }
            

    #上のreturnが実行されなかったら普通に全ユーザーモデルを表示する
    context = {
        "info": info,
        "form": form,
    }
    return render(request, "myapp/friends.html", context)
"""

@login_required
def friends(request):
    user = request.user

    latest_msg = Talk.objects.filter(
        Q(talk_from=OuterRef("pk"), talk_to=user)
        | Q(talk_from=user, talk_to=OuterRef("pk"))
    ).order_by("-time")
    
    friends = (
        User.objects.exclude(id=user.id)
        .annotate(
            latest_msg_talk=Subquery(latest_msg.values("talk")[:1]),
            latest_msg_time=Subquery(latest_msg.values("time")[:1]),
        )
        .order_by(F("latest_msg_time").desc(nulls_last=True))
    )
    
    #検索機能
    form = FriendsSearchForm()

    if request.method == "GET" and "friends_search" in request.GET:
        form = FriendsSearchForm(request.GET)

        # 送信内容があった場合
        if form.is_valid():
            keyword = form.cleaned_data.get("keyword")
            # 何も入力せずに検索した時に全件を表示するようにするため、分岐しておく
            if keyword:
                # 入力に対して部分一致する友達を絞り込む
                friends = friends.filter(
                    Q(username__icontains=keyword)            # ユーザーネームの部分一致
                    | Q(email__icontains=keyword)             # メールアドレスの部分一致
                    | Q(latest_msg_talk__icontains=keyword)   # 最新のトーク内容の部分一致
                )

                request.session["keyword"] = request.GET

                # friendsに何らか情報があったとき
                context = {
                    "friends": friends,
                    "form": form,
                    # 検索結果を表示する画面にするために、そうであることを明示する変数を作る
                    "is_searched": True,
                }
                return render(request, "myapp/friends.html", context)

    # ここまでが検索機能

    # POSTでない（リダイレクトorただの更新）& 検索欄に入力がない場合
    context = {
        "friends": friends,
        "form": form,
    }
    return render(request, "myapp/friends.html", context)

@login_required
def talk_room(request, user_id):
    user = request.user
    friend = get_object_or_404(User, id=user_id)
    #friend = User.objects.get(id=user_id)と書いてもいいわけね
    talk = Talk.objects.filter(
        Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
    ).order_by("time")
    form = TalkForm()
    context = {
        "form": form,
        "talk": talk,
        "friend": friend,
    }

    if request.method == "POST":
        #ユーザーにはメッセージ内容のフィールドだけPOSTさせておいて、他のフィールドはこちらで入力する
        new_talk = Talk(talk_from=user, talk_to=friend)
        form = TalkForm(request.POST, instance=new_talk)

        if form.is_valid():
            form.save()
            # このようなリダイレクト処理はPOSTのリクエストを初期化し、リクエストをGETに戻すことにより
            # 万一更新処理を連打されてもPOSTのままにさせない等の用途がある
            return redirect("talk_room", user_id)
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

    # POSTでない（リダイレクトorただの更新）&POSTでも入力がない場合
    return render(request, "myapp/talk_room.html", context)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def user_img_change(request):
    user = request.user
    if request.method == "GET":
        # モデルフォームには `instance=user` をつけることで user の情報が入った状態のフォームを参照できます。
        # 今回はユーザ情報の変更の関数が多いのでこれをよく使います。
        form = ImageSettingForm(instance=user)

    elif request.method == "POST":
        form = ImageSettingForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("friends")
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/user_img_change.html", context)

@login_required
def mail_change(request):
    user = request.user
    if request.method == "GET":
        form = MailSettingForm(instance=user)

    elif request.method == "POST":
        form = MailSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("friends")
        else:
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/mail_change.html", context)

@login_required
def username_change(request):
    user = request.user
    if request.method == "GET":
        form = UserNameSettingForm(instance=user)

    elif request.method == "POST":
        form = UserNameSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("username_change_done")
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/username_change.html", context)

class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("index")
    template_name = "myapp/password_change.html"

