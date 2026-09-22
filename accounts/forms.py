from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):

    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your full name'
            }
        )
    )

    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your phone number'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Create a password'
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password'
            }
        )
    )

    terms = forms.BooleanField(
        required=True,
        error_messages={
            'required': 'You must agree to the Terms & Conditions.'
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This username is already taken.'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'An account with this email already exists.'
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    'Passwords do not match.'
                )

        return cleaned_data

    class Meta:
        model = User

        fields = [
            'username',
            'email',
        ]