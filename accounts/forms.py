from django import forms
from django.contrib.auth.models import User
from accounts.models import StudentProfile

# Registration form
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

# Login Form

class LoginForm(forms.Form):

    username_or_email = forms.CharField(
        label='Username or Email',
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your username or email'
            }
        )
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password'
            }
        )
    )

class ProfileForm(forms.ModelForm):

    class Meta:

        model = StudentProfile

        fields = [
            'phone',
            'date_of_birth',
            'location',
            'college',
            'degree',
            'year_of_passing',
            'cgpa',
            'career_goal',
            'areas_of_interest',
            'skills',
            'preferred_job_role',
            'preferred_location',
            'willing_to_relocate',
        ]

        widgets = {

            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your phone number'
                }
            ),

            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your location'
                }
            ),

            'college': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your college or university'
                }
            ),

            'degree': forms.TextInput(
                attrs={
                    'placeholder': 'Example: B.Tech Computer Science'
                }
            ),

            'year_of_passing': forms.NumberInput(
                attrs={
                    'placeholder': 'Example: 2025'
                }
            ),

            'cgpa': forms.NumberInput(
                attrs={
                    'placeholder': 'Example: 8.60',
                    'step': '0.01'
                }
            ),

            'career_goal': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Python Backend Developer'
                }
            ),

            'areas_of_interest': forms.Textarea(
                attrs={
                    'placeholder': 'Example: Backend Development, APIs, AI',
                    'rows': 3
                }
            ),

            'skills': forms.Textarea(
                attrs={
                    'placeholder': 'Example: Python, Django, SQL, PostgreSQL',
                    'rows': 3
                }
            ),

            'preferred_job_role': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Backend Developer'
                }
            ),

            'preferred_location': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Bengaluru'
                }
            ),

            'willing_to_relocate': forms.CheckboxInput()
        }