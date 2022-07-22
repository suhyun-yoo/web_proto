from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('agreement/', views.AgreementView.as_view(), name='agreement'),
    path('csregister/', views.CsRegisterView.as_view(), name='csregister'),
    path('registerauth/', views.register_success, name='register_success'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
    #path('main/', views.main_view, name='main'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recovery/id/', views.RecoveryIdView.as_view(), name='recovery_id'),
    path('recovery/id/find/', views.ajax_find_id_view, name='ajax_id'),
]
