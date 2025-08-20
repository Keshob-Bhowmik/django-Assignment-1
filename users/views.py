from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm, CustomRegistrationForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
def sign_up(request):

    form = CustomRegistrationForm()
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print('user', user)
            user.set_password(form.cleaned_data.get('password1'))
            print(form.cleaned_data)
            user.is_active = False
            user.save()
            messages.success(request, 'A activation mail is sent. Please check your mail')
            return redirect('sign_in')
            
    return render(request, 'registration/sign_up.html', {'form':form})

def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('Home')
    return render(request, 'registration/sign_in.html', {'form' : form})

@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('Home')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign_in')
        else:
            return HttpResponse("Invalid Id or token")
    except User.DoesNotExist:
        return HttpResponse("User does not exist")
