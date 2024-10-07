from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path('friends/', views.friends, name='friends'),
    path("talk_room/<int:user_id>/", views.talk_room, name="talk_room"),
    path('setting/', views.setting, name='setting'),
    path("password_change/", views.PasswordChange.as_view(), name="password_change"),
    # path("password_change_done/", views.PasswordChangeDone.as_view(), name="password_change_done"),
    path("user_img_change/", views.user_img_change, name="user_img_change"),
    # path("user_img_change_done/", views.user_img_change_done, name="user_img_change_done"),
    path("mail_change/", views.mail_change, name="mail_change"),
    # path("mail_change_done/", views.mail_change_done, name="mail_change_done"),
    path("username_change/", views.username_change, name="username_change"),
    # path("username_change_done/", views.username_change_done, name="username_change_done"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)