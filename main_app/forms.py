from django import forms
from django.forms import ModelForm
from .models import Listen
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ListenForm(ModelForm):
    class Meta:
        model = Listen
        fields = ['date', 'time']
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
            'time': forms.Select(
                attrs={
                    'class': 'browser-default'
                }
            )
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password2'].label = "Confirm Password"
