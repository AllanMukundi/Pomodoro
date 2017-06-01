from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    """
    A form that lets a user login.
    """
    username = forms.CharField(label='',
            widget=forms.TextInput
            (attrs={'placeholder': 'Username', 'class': 'login-field'}))
    password = forms.CharField(label='',
            widget=forms.PasswordInput
            (attrs={'placeholder': 'Password', 'class': 'login-field'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class RegistrationForm(UserCreationForm):
    """
    A form that lets a user register.
    """
    username = forms.Field(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(required=True, max_length=254, widget=forms.TextInput
            (attrs={'placeholder': 'Email'}))
    password1 = forms.Field(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.Field(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

class TestForm(PasswordChangeForm):

    old_password = forms.CharField(
        label=(''),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'placeholder': 'Old password'}),
    )
    new_password1 = forms.CharField(
        label=(''),
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}),
        strip=False,
        help_text= None,
    )
    new_password2 = forms.CharField(
        label=(''),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )

    class Meta:
        help_text = {
        'new_password1': None
        }
