from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='quotes:root')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='users:login')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='quotes:root')

    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'), password=request.POST.get('password'))
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect('users:login')

        login(request, user)
        return redirect('quotes:root')

    return render(request, 'users/login.html', {"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='quotes:root')
