from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# User sign up form extending UserCreationForm
class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password2 = forms.CharField(label="Confirm Password",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'autocomplete': 'off'}))
    email = forms.CharField(label="Email", max_length=120, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    # removing colon after labels
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UserSignupForm, self).__init__(*args, **kwargs)


# User Profile form
class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, error_messages={'invalid': "Image files only."},
                                       widget=forms.FileInput, label="Profile Picture")
    status = forms.CharField(required=False, error_messages={'invalid': "This field is required."},
                             widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=200)
    profile_visibility = forms.BooleanField(required=False,
                                            widget=forms.CheckboxInput(
                                                attrs={'class': 'form-check-input'}),
                                            label="Make your profile visible to users you are not friend with?")

    class Meta:
        model = UserProfile
        fields = ('avatar', 'status', 'profile_visibility')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UserProfileForm, self).__init__(*args, **kwargs)


# User form
class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email", max_length=120, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


# Post form
class PostForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Have something to share? Tell us here!', 'rows': 5}),
        label="Tell us something!")
    image = forms.ImageField(required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput,
                             label="Add an image (Optional)")

    class Meta:
        model = UserPost
        fields = ['text', 'image']
