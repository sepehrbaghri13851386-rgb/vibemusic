from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import secrets

from .models import CustomUser


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # اعتبارسنجی ساده
        if not username or not email or not password or not password2:
            messages.error(request, 'لطفاً همه‌ی فیلدها را پر کنید.')
            return render(request, 'signup.html')

        if password != password2:
            messages.error(request, 'رمز عبور و تکرار آن یکسان نیستند.')
            return render(request, 'signup.html')

        if len(password) < 8:
            messages.error(request, 'رمز عبور باید حداقل ۸ کاراکتر باشد.')
            return render(request, 'signup.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'این نام کاربری قبلاً استفاده شده است.')
            return render(request, 'signup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'این ایمیل قبلاً ثبت شده است.')
            return render(request, 'signup.html')

        # ساخت کاربر جدید با پسورد هش‌شده
        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=make_password(password),
        )

        # لاگین خودکار بعد از ثبت‌نام (ذخیره‌ی آیدی کاربر در session)
        request.session['user_id'] = user.id
        messages.success(request, f'خوش آمدید {username}! ثبت‌نام با موفقیت انجام شد.')
        return redirect('home')

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        next_url = request.POST.get('next') or request.GET.get('next')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
            return render(request, 'signin.html')

        if not check_password(password, user.password):
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
            return render(request, 'signin.html')

        request.session['user_id'] = user.id

        if next_url:
            return redirect(next_url)
        return redirect('home')

    return render(request, 'signin.html')


def logout_view(request):
    request.session.flush()
    return redirect('home')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        user = CustomUser.objects.filter(email=email).first()

        if user:
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.reset_token_created = timezone.now()
            user.save(update_fields=['reset_token', 'reset_token_created'])

            reset_link = request.build_absolute_uri(
                reverse('reset_password', args=[token])
            )
            send_mail(
                subject='بازیابی رمز عبور Vibe Music',
                message=f'برای تنظیم رمز عبور جدید روی لینک زیر بزنید (تا ۳۰ دقیقه معتبر است):\n{reset_link}',
                from_email='no-reply@vibemusic.local',
                recipient_list=[email],
                fail_silently=True,
            )

        messages.success(request, 'اگر این ایمیل در سیستم ثبت شده باشد، لینک بازیابی رمز برایش ارسال شد.')
        return redirect('forgot_password')

    return render(request, 'forgot-password.html')


def reset_password_view(request, token):
    user = CustomUser.objects.filter(reset_token=token).first()

    valid = False
    if user and user.reset_token_created:
        if timezone.now() - user.reset_token_created <= timedelta(minutes=30):
            valid = True

    if not valid:
        messages.error(request, 'لینک بازیابی نامعتبر یا منقضی شده است.')
        return redirect('forgot_password')

    if request.method == 'POST':
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if len(password) < 8:
            messages.error(request, 'رمز عبور باید حداقل ۸ کاراکتر باشد.')
            return render(request, 'reset-password.html', {'token': token})

        if password != password2:
            messages.error(request, 'رمز عبور و تکرار آن یکسان نیستند.')
            return render(request, 'reset-password.html', {'token': token})

        user.password = make_password(password)
        user.reset_token = None
        user.reset_token_created = None
        user.save(update_fields=['password', 'reset_token', 'reset_token_created'])

        messages.success(request, 'رمز عبور با موفقیت تغییر کرد. حالا وارد شوید.')
        return redirect('signin')

    return render(request, 'reset-password.html', {'token': token})
