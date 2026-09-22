from django.shortcuts import render,redirect
from accounts.forms import RegistrationForm
# Create your views here.
from accounts.models import EmailVerification
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.urls import reverse


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