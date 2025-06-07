from django import forms
from captcha.fields import CaptchaField
from main.models import *



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('__all__')
    captcha = CaptchaField()