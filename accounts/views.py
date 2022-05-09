from accounts.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .forms import SignInForm, SignUpForm
from django.contrib import messages
from .utils import send_activation_email, generate_token
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            send_activation_email(request, user)
            return redirect('accounts:verify')
        messages.error(request, "Unsuccessful registration.")
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if not user.is_email_verified:
                    send_activation_email(request, user)
                    return redirect('accounts:verify')

                return redirect('app:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = SignInForm()
    return render(request, 'accounts/signin.html', {'form': form})

@login_required(login_url='accounts:login', redirect_field_name='')
def verify(request):
    if request.user.is_email_verified:
        return redirect('app:home')

    return render(request, 'accounts/verify-email.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return redirect('app:home')

    return redirect('accounts:verify')

@login_required(login_url='accounts:login', redirect_field_name='')
def signout(request):
    logout(request)
    return redirect('accounts:login')

@login_required(login_url='accounts:login', redirect_field_name='')
def resend(request):
    if request.user.is_email_verified:
        return redirect("app:home")

    send_activation_email(request, request.user)
    messages.success(request, 'A new verification link has been sent to the email address you provided during registration.')
    return redirect('accounts:verify')