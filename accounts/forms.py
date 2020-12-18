from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Interest, Subscriber


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("이미 존재하는 이메일입니다.")
        return email


class ProfileForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = '__all__'
        exclude = ['user']


class InterestForm(ModelForm):
    class Meta:
        model = Interest
        fields = '__all__'
        # exclude = ['subscriber']
        # fields = ['hobby', 'detail']
