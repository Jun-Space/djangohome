from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import *

from .models import Subscriber
from .tokens import account_activation_token


def login_page(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    else:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            password = request.POST.get('password')

            user = authenticate(request, username=user_id, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, '존재하지 않는 ID 이거나 패스워드가 틀립니다.')
        context = {}
        return render(request, 'login_page.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = '가입을 확인하세요'
                message = render_to_string('activate_email.html',
                                           {
                                               'user': user,
                                               'domain': current_site.domain,
                                               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                               'token': account_activation_token.make_token(user),
                                           })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('이메일에서 인증을 진행해주세요!')
        else:
            form = CreateUserForm()
        return render(request, 'register_page.html', {'form': form})


# def register_page(request):
#     if request.user.is_authenticated:
#         return redirect('user_dashboard')
#     else:
#         form = CreateUserForm()
#         if request.method == 'POST':
#             form = CreateUserForm(request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 user_id = form.cleaned_data.get('username')
#                 messages.success(request, user_id + '계정이 성공적으로 생성되었습니다.')
#                 return redirect('login')
#         context = {'form': form}
#         return render(request, 'register_page.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('유효하지 않은 링크입니다.')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def user_dashboard(request):
    username = request.user.username
    subscriber = request.user.subscriber
    interests = request.user.subscriber.interest_set.all()
    context = {'interests': interests, 'subscriber': subscriber,
               'username': username}
    return render(request, 'user_dashboard.html', context)


def edit_profile(request):
    subscriber = request.user.subscriber
    form = ProfileForm(instance=subscriber)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=subscriber)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    context = {'form': form}
    return render(request, 'edit_profile.html', context)


@login_required(login_url='login')
def create_interest(request):  # 여기서 form에서 subscriber는 새로 등록하지 않고 해당 로그인된 사용자로 자동으로 등록하게 하고 싶다
    form = InterestForm()
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    context = {'form': form}
    return render(request, 'create_interest.html', context)


def update_interest(request, pk_id):
    interest = Interest.objects.get(id=pk_id)
    form = InterestForm(instance=interest)
    if request.method == 'POST':
        form = InterestForm(request.POST, instance=interest)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')

    context = {'form': form}
    return render(request, 'create_interest.html', context)


def delete_interest(request, pk_id):
    interest = Interest.objects.get(id=pk_id)

    if request.method == 'POST':
        interest.delete()
        return redirect('user_dashboard')

    context = {'interest': interest}
    return render(request, 'delete_interest.html', context)


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    else:
        return redirect('login')
