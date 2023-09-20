from random import randint

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from .forms import (
    ProfileOtpCheckForm,
    ProfileUpdateForm,
    UserSignInForm,
    UserSignUpForm,
    UserUpdateForm,
)


def send_mail(from_email, to_email, username, otp_code):
    html_content = render_to_string( 
            'user_profiles/mail_otp.html',
            {
                'username': username,
                'otp_code': otp_code,
            }
        )
    subj = 'Your OTP code'
    msg = EmailMultiAlternatives(
        subject=subj,
        body=subj,
        from_email=from_email,
        to=[to_email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def sign_in(request):
    form = UserSignInForm(request.POST)
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            user.profile.otp = randint(100000, 999999)
            user.profile.save()
            request.session['username'] = username
            send_mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_email=user.email,
                username=username,
                otp_code=user.profile.otp
            )
            messages.success(request, "Your OTP has been send to your email.")
            return redirect("otp_check")
        else:
            messages.error(request, "Wrong Credentials!!")
    else:
        form = UserSignInForm()
    return render(request, 'user_profiles/sign_in.html', {'form': form})



def otp_check(request):
    username = request.session['username']
    otp_form = ProfileOtpCheckForm(request.POST)
    if request.method == "POST":
        otp = request.POST.get('otp')
        user = User.objects.filter(username = username).first()
        if int(otp) == user.profile.otp:
            messages.success(request, 'OTP Success!')
            login(request, user)
            messages.success(request, f' Wecome {request.user.username}')
            user.profile.otp = 0
            user.profile.save()
            return redirect('bbs:main')
        else:
            messages.error(request, "Wrong OTP!!")
    else:
        otp_form = ProfileOtpCheckForm()
    return render(request, "user_profiles/otp_check.html", {'form': otp_form})



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('user_profiles:profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'user_profiles/profile.html', context)

@login_required
def sign_out(request):
    logout(request)
    messages.success(request, 'Succesfully signed out!')
    return redirect('bbs:main')


def sign_up(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('sign_in')
    else:
        form = UserSignUpForm()
    return render(request, 'user_profiles/sign_up.html', {'form': form})