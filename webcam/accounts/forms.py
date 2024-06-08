from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Memo
from datetime import date

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = [ 'text', 'photo']
        date = forms.DateField(initial=date.today(), widget=forms.TextInput(attrs={'readonly':'readonly'}))