from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('main/', views.main_view, name='main'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('agreement/', views.AgreementView.as_view(), name='agreement'),
    path('csregister/', views.CsRegisterView.as_view(), name='csregister'),
    path('registerauth/', views.register_success, name='register_success'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),

    path('recovery/id/', views.RecoveryIdView.as_view(), name='recovery_id'),
    path('recovery/pw/', views.RecoveryPwView.as_view(), name='recovery_pw'),
    path('recovery/id/find/', views.ajax_find_id_view, name='ajax_id'),
    path('recovery/pw/find/', views.ajax_find_pw_view, name='ajax_pw'),
    path('recovery/pw/auth/', views.auth_confirm_view, name='recovery_auth'),
    path('recovery/pw/reset/', views.auth_pw_reset_view, name='recovery_pw_reset'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile_update'),


]
