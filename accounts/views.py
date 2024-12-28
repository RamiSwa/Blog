from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import LogoutView

from django.contrib.auth import get_user_model
from django.http import HttpResponse

from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

def register(request):
    """Allow users to register."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate user until email is confirmed
            user.save()

            # Generate token and build confirmation URL
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirmation_url = request.build_absolute_uri(
                reverse('email_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            # Send confirmation email
            send_mail(
                'Confirm Your Email Address',
                f'Hi {user.username},\n\n'
                f'Thank you for registering at My Blog. Please confirm your email address by clicking the link below:\n\n'
                f'{confirmation_url}\n\n'
                f'If you did not register, please ignore this email.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Registration successful. A confirmation email has been sent to your inbox.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})




@login_required
def profile(request):
    """Allow users to view and update their profile."""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # Send profile update email
            send_mail(
                'Profile Updated',
                f'Hi {request.user.username},\n\nYour profile has been successfully updated.',
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
            messages.success(request, 'Profile updated successfully. A confirmation email has been sent.')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def dashboard(request):
    """Show the user dashboard."""
    return render(request, 'accounts/dashboard.html')





class CustomPasswordChangeView(PasswordChangeView):
    def form_valid(self, form):
        user = self.request.user
        send_mail(
            'Password Changed Successfully',
            f'Hi {user.username},\n\nYour password has been successfully changed.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)





User = get_user_model()

def email_confirm(request, uidb64, token):
    """Confirm the user's email address."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been confirmed. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'The confirmation link is invalid or has expired.')
        return redirect('register')
    
    
    

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)
