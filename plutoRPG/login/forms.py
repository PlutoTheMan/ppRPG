from django import forms

class LoginForm(forms.Form):
    """Representing Login Form"""
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your name'}), max_length=100)
    password = forms.CharField(widget=forms.PasswordInput({'placeholder': 'Your password'}), label='Password')


