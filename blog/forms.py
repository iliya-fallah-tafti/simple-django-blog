from django import forms
from .models import Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentForm(forms.ModelForm):
    # recaptcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    class Meta:
        model = Comment
        fields = ['post','name', 'email', 'subject','message']