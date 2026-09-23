from django.shortcuts import render,redirect
from accounts.forms import RegistrationForm,LoginForm,ProfileForm
# Create your views here.
from accounts.models import EmailVerification
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User

def register(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            full_name = form.cleaned_data['full_name']
            password = form.cleaned_data['password']

            # Store full name
            user.first_name = full_name

            # Account remains inactive until email verification
            user.is_active = False

            # Hash the password
            user.set_password(password)

            # Save user to database
            user.save()

            # Create email verification record
            verification = EmailVerification.objects.create(
                user=user,
                expires_at=timezone.now() + timedelta(hours=1)
            )

            # Create verification URL
            verification_url = request.build_absolute_uri(
                reverse(
                    'verify_email',
                    args=[verification.token]
                )
            )

            # Send verification email
            send_mail(
                subject='Verify your CareerPilot account',
                message=(
                    f'Hello {full_name},\n\n'
                    'Welcome to CareerPilot!\n\n'
                    'Please verify your email address by clicking '
                    'the link below:\n\n'
                    f'{verification_url}\n\n'
                    'This verification link will expire in 1 hour.\n\n'
                    'If you did not create this account, '
                    'you can ignore this email.'
                ),
                from_email=None,
                recipient_list=[user.email],
            )

            print("User created successfully!")
            print("Email verification record created!")
            print("Verification email generated!")

            # Show Check Your Email page
            return render(
                request,
                'accounts/check_email.html',
                {
                    'email': user.email
                }
            )

    else:
        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def verify_email(request, token):

    try:
        verification = EmailVerification.objects.get(
            token=token
        )

    except EmailVerification.DoesNotExist:
        return render(
            request,
            'accounts/email_verification.html',
            {
                'status': 'invalid'
            }
        )

    # Check if the verification link was already used
    if verification.is_used:
        return render(
            request,
            'accounts/email_verification.html',
            {
                'status': 'used'
            }
        )

    # Check if the verification link has expired
    if timezone.now() > verification.expires_at:
        return render(
            request,
            'accounts/email_verification.html',
            {
                'status': 'expired'
            }
        )

    # Activate the user's account
    user = verification.user
    user.is_active = True
    user.save()

    # Mark verification token as used
    verification.is_used = True
    verification.save()

    return render(
        request,
        'accounts/email_verification.html',
        {
            'status': 'success',
            'user': user
        }
    )

def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            username_or_email = form.cleaned_data[
                'username_or_email'
            ]

            password = form.cleaned_data['password']

            # Check whether the user entered an email
            if '@' in username_or_email:

                try:
                    user_obj = User.objects.get(
                        email=username_or_email
                    )

                    username = user_obj.username

                except User.DoesNotExist:
                    username = username_or_email

            else:
                username = username_or_email

            # Authenticate the user
            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                # Check whether email has been verified
                if not user.is_active:

                    messages.error(
                        request,
                        'Please verify your email address before logging in.'
                    )

                    return render(
                        request,
                        'accounts/login.html',
                        {'form': form}
                    )

                # Create login session
                login(request, user)

                messages.success(
                    request,
                    'Welcome back!'
                )

                return redirect('home')

            else:

                messages.error(
                    request,
                    'Invalid username/email or password.'
                )

    else:

        form = LoginForm()

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )
def logout_view(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect('home')

def profile_view(request):

    if not request.user.is_authenticated:
        return redirect('login')

    profile = request.user.student_profile

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Your profile has been updated successfully.'
            )

            return redirect('profile')

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'accounts/profile.html',
        {
            'form': form
        }
    )