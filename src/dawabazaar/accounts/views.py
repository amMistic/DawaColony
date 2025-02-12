from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth import decorators, authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SellerRegistrationForm, UserRegistrationForm
from django.contrib import messages
from functools import wraps
from typing import List
from .models import User


# custome authentication method with role check
def auth_required(allowed_roles: List[str] = []):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapper_view(request, *args, **kwargs):
            # check user authentication
            if not request.user.is_authenticated:
                return redirect("accounts:register")

            # check the role
            if allowed_roles and request.user.role not in allowed_roles:
                return redirect("pages:no-access")
            return view_func(request, *args, **kwargs)

        return _wrapper_view

    return decorator


# Create your views here.
def seller_register_view(request):
    form = SellerRegistrationForm()
    if request.method == "POST":
        form = SellerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # form.save()
                user = form.save(commit=False)
                user.role = 'Seller'
                user.save()
                messages.success(request, "User Created Successfully")
                return redirect("accounts:login")
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)

        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    context = {"form": form}
    return render(request, "accounts/seller_register.html", context)


def customer_register_view(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Create Sucessfully")
            return redirect("accounts:login")
        else:
            messages.error(
                request, "Error geting user information!! Please, Try again later :("
            )

    context = {"form": form}
    return render(request, "accounts/customer_register.html", context)


def login_user_view(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user and user.role == 'Seller':
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("seller:dashboard")
            
            elif user and user.role == 'Customer':
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("pages:home")
            
            messages.error(request, "Invalid username or password!")

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("pages:home")
