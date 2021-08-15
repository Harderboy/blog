from django.urls import path
from users.views import RegisterView, ImageCodeView, SmsCodeView, LoginView, LogoutView, ForgetPasswordView,\
    UserCenterView, WriteBlogView

#
# app_name = 'users'
urlpatterns = [
    # path 第一参数：路由
    # 注册路由
    path('register/', RegisterView.as_view(), name='register'),
    # 验证码
    path('imagecode/', ImageCodeView.as_view(), name='imagecode'),
    # 短信验证码
    path('smscode/', SmsCodeView.as_view(), name='smscode'),
    # 登录
    path('login/', LoginView.as_view(), name='login'),
    # 退出登录
    path('logout/', LogoutView.as_view(), name='logout'),
    # 忘记密码
    path('forgetpassword/', ForgetPasswordView.as_view(), name='forgetpassword'),
    # 个人中心
    path('center/', UserCenterView.as_view(), name='center'),
    # 写博客
    path('writeblog/',WriteBlogView.as_view(), name="writeblog")
]
