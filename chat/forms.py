from logging import PlaceHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput
from .models import UserProfile, Conversations, Message

class UserSignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Re-Enter Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        widgets = {
        'username': forms.fields.TextInput(attrs={'placeholder': 'Username'}),
        'first_name': forms.fields.TextInput(attrs={'placeholder': 'Name'}),
        'email': forms.fields.TextInput(attrs={'placeholder': 'Email'}),
        }


class CustomAuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']

    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}) 
        self.fields['password'].label = False

class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ['email']
    
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        self.fields['email'].label = False

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}), required=False)
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class NewChatForm(forms.ModelForm):
    participant_2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter contacts username here...'}))
    class Meta:
        model = Conversations
        exclude = ['participant_1', 'participant_2', 'thread_name']
