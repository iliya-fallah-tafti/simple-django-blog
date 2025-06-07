from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from .forms import *
from django.utils.encoding import force_bytes
from .forms import PasswordResetRequestForm
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SetNewPasswordForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login


# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = CaptchaAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "The username or password is incorrect.")
        else:
            messages.error(request, "Please enter the information correctly.")
    else:
        form = CaptchaAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required(login_url="/accounts/login")
def logout_view(request):
    logout(request)
    return redirect('/')


# def logout_view(request):
#     if request.user.is_authenticated:
#         logout(request)
#         return redirect('/')
#     return redirect('/')

# فرم ثبت نام بدوم ایمیل
# def signup_view(request):
#     if not request.user.is_authenticated:
#         if request.method == "POST":
#             form = UserCreationForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect(reverse('accounts:login'))
#         form = UserCreationForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'accounts/signup.html', context)
#     else:
#         return redirect('/')

# فرم ثبت نام با ایمیل
from django.urls import reverse
from .forms import CustomUserCreationForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully. You can now log in.")
            return redirect(reverse('accounts:login'))
        else:
            messages.error(request, "Please complete the fields correctly.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


@login_required(login_url="/accounts/login")
def profile_view(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})


@login_required(login_url="/accounts/login")
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})


User = get_user_model()


def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email__iexact=email).first()
            if user:
                token = PasswordResetTokenGenerator().make_token(user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(f'/accounts/reset/{uidb64}/{token}/')

                # ایمیل را ارسال می‌کنیم
                subject = 'Password Reset Request'
                message = render_to_string('accounts/password_reset_email.html', {
                    'reset_link': reset_link,
                    'user': user,
                })
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return render(request, 'accounts/password_reset_done.html')

    else:
        form = PasswordResetRequestForm()

    return render(request, 'accounts/password_reset_form.html', {'form': form})


from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from .forms import SetNewPasswordForm


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            messages.error(request, "The password reset link is invalid.")
            return render(request, 'accounts/password_reset_invalid.html')

    except Exception:
        messages.error(request, "The password reset link is invalid.")
        return render(request, 'accounts/password_reset_invalid.html')

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(request, "Your password has been successfully changed.")
            return redirect('accounts:login')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
    else:
        form = SetNewPasswordForm()

    return render(request, 'accounts/password_reset_confirm.html', {'form': form})


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import timedelta
from django.utils import timezone


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.last_login) + str(timezone.now())

    def check_token(self, user, token):
        expiration_time = timedelta(hours=1)
        token_time = self._parse_token(token)[1]
        if timezone.now() - token_time > expiration_time:
            return False
        return super().check_token(user, token)
