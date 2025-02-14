from django.urls import path
from . import views

app_name="accounts"
urlpatterns = [
    path("register/",views.RegisterUserView.as_view(),name="register"),
    path("verify/",views.VerifyRegisterCodeView.as_view(),name="verify"),
    path("login/",views.LoginUserView.as_view(),name="login"),
    path("logout/",views.LogoutUserView.as_view(),name="logout"),
    path("change_password/<int:type>/",views.ChangePasswordView.as_view(),name="change_password"),
    path("SendCode/",views.SendCodeView.as_view(),name="SendCode"),
    path("AuthCode/",views.AuthCodeView.as_view(),name="AuthCode"),
    
    path("userpanel/",views.UserPanelView.as_view(),name="userpanel"),
    path("show_last_orders/",views.show_last_orders,name="show_last_orders"),
    path("update_profile/",views.UpdateProfileView.as_view(),name="update_profile"),
    path("show_user_payments/",views.show_user_payments,name="show_user_payments"),
]
