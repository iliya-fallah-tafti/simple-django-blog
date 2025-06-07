# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="email")


from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        try:
            validate_password(password1)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField


class CaptchaAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
