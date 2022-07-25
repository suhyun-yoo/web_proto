from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from .decorators import *
from .models import User
from django.views.generic import View,CreateView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import CsRegisterForm, LoginForm, RecoveryPwForm, CustomSetPasswordForm
from django.urls import reverse
from .helper import send_mail, email_auth_num
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login, logout, authenticate
from django.views.generic import FormView
from django.conf import settings
from django.core.exceptions import ValidationError
from .forms import RecoveryIdForm, CustomCsUserChangeForm
from django.views.generic import View
import json
from django.core.serializers.json import DjangoJSONEncoder


@login_message_required
def main_view(request):
    return render(request, 'main/main.html')

# 회원가입
class CsRegisterView(CreateView):
    model = User
    template_name = 'accounts/register_cs.html'
    form_class = CsRegisterForm

    def get(self, request, *args, **kwargs):
        if not request.session.get('agreement', False):
            raise PermissionDenied
        request.session['agreement'] = False
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        self.request.session['register_auth'] = True
        messages.success(self.request, '회원님의 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다.')
        return reverse('accounts:register_success')


    def form_valid(self, form):
        self.object = form.save()

        send_mail(
            '{}님의 회원가입 인증메일 입니다.'.format(self.object.user_id),
            [self.object.email],
            html=render_to_string('accounts/register_email.html', {
                'user': self.object,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
                'domain': self.request.META['HTTP_HOST'],
                'token': default_token_generator.make_token(self.object),
            }),
        )
        return redirect(self.get_success_url())

# 이메일 인증 활성화
def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('accounts:login')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('accounts:login')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('accounts:login')

@login_message_required
def main_view(request):
    return render(request, 'main/main.html')

# 회원가입 약관동의
@method_decorator(logout_message_required, name='dispatch')
class AgreementView(View):
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False
        return render(request, 'accounts/agreement.html')

    def post(self, request, *args, **kwarg):
        if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
            request.session['agreement'] = True

            if request.POST.get('csregister') == 'csregister':
                return redirect('../csregister/')
        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'accounts/agreement.html')

# 회원가입 인증메일 발송 안내 창
def register_success(request):
    if not request.session.get('register_auth', False):
        raise PermissionDenied
    request.session['register_auth'] = False

    return render(request, 'accounts/register_success.html')

# 로그인
@method_decorator(logout_message_required, name='dispatch')
class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = '../main/'


    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=user_id, password=password)
        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user)
            remember_session = self.request.POST.get('remember_session', False)


        return super().form_valid(form)

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('/')

# 비밀번호찾기
@method_decorator(logout_message_required, name='dispatch')
class RecoveryPwView(View):
    template_name = 'accounts/recovery_pw.html'
    recovery_pw = RecoveryPwForm

    def get(self, request):
        if request.method=='GET':
            form = self.recovery_pw(None)
            return render(request, self.template_name, { 'form':form, })

# 아이디찾기 AJAX 통신
def ajax_find_pw_view(request):
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    email = request.POST.get('email')
    target_user = User.objects.get(user_id=user_id, name=name, email=email)

    if target_user:
        auth_num = email_auth_num()
        target_user.auth = auth_num
        target_user.save()

        # send_mail(
        #     '비밀번호 찾기 인증메일입니다.',
        #     [email],
        #     html=render_to_string('accounts/recovery_email.html', {
        #         'auth_num': auth_num,
        #     }),
        # )
    return HttpResponse(json.dumps({"result": target_user.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")

# 비밀번호찾기 인증번호 확인
def auth_confirm_view(request):
    user_id = request.POST.get('user_id')
    input_auth_num = request.POST.get('input_auth_num')
    target_user = User.objects.get(user_id=user_id, auth=input_auth_num)
    target_user.auth = ""
    target_user.save()
    request.session['auth'] = target_user.user_id

    return HttpResponse(json.dumps({"result": target_user.user_id}, cls=DjangoJSONEncoder),
                        content_type="application/json")


@logout_message_required
def auth_pw_reset_view(request):
    if request.method == 'GET':
        if not request.session.get('auth', False):
            raise PermissionDenied

    if request.method == 'POST':
        session_user = request.session['auth']
        current_user = User.objects.get(user_id=session_user)
        login(request, current_user)

        reset_password_form = CustomSetPasswordForm(request.user, request.POST)

        if reset_password_form.is_valid():
            user = reset_password_form.save()
            messages.success(request, "비밀번호 변경완료! 변경된 비밀번호로 로그인하세요.")
            logout(request)
            return redirect('accounts:login')
        else:
            logout(request)
            request.session['auth'] = session_user
    else:
        reset_password_form = CustomSetPasswordForm(request.user)

    return render(request, 'accounts/password_reset.html', {'form': reset_password_form})


@method_decorator(logout_message_required, name='dispatch')
class RecoveryIdView(View):
    template_name = 'accounts/recovery_id.html'
    form = RecoveryIdForm

    def get(self, request):
        if request.method=='GET':
            form = self.recovery_id(None)
        return render(request, self.template_name, { 'form':form, })


def ajax_find_id_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_id = User.objects.get(name=name, email=email)

    return HttpResponse(json.dumps({"result_id": result_id.user_id}, cls=DjangoJSONEncoder),
                        content_type="application/json")


# 아이디찾기
@method_decorator(logout_message_required, name='dispatch')
class RecoveryIdView(View):
    template_name = 'accounts/recovery_id.html'
    recovery_id = RecoveryIdForm

    def get(self, request):
        if request.method=='GET':
            form_id = self.recovery_id(None)
        return render(request, self.template_name, { 'form_id':form_id, })


def ajax_find_id_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_id = User.objects.get(name=name, email=email)

    return HttpResponse(json.dumps({"result_id": result_id.user_id}, cls=DjangoJSONEncoder),
                        content_type="application/json")

def main(request):
    return render(request, 'main/main.html')

@login_message_required
def profile_view(request):
    if request.method == 'GET':
        return render(request, 'accounts/profile.html')


@login_message_required
def profile_update_view(request):
    if request.method == 'POST':
        user_change_form = CustomCsUserChangeForm(request.POST, instance = request.user)

        if user_change_form.is_valid():
            user_change_form.save()
            messages.success(request, '회원정보가 수정되었습니다.')
            return render(request, 'accounts/profile.html')
    else:
        user_change_form = CustomCsUserChangeForm(instance = request.user)

        return render(request, 'accounts/profile_update.html', {'user_change_form':user_change_form})

