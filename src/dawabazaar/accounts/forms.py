from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SellerRegistrationForm(UserCreationForm):
    """
    Form for user who want to become a seller on our platform - DawaBazaar!
    """

    username = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "Placeholder": "Steff Oberoi"}
        ),
    )

    email = forms.EmailField(
        max_length=64,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "oberois.chemist@gmail.com",
            }
        ),
    )

    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+916354785139"}
        ),
    )

    shopname = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Oberoi's Chemist"}
        ),
    )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "Placeholder": "shop-13 Rohan Society, near lala circle, Rajkot, India",
                "class": "form-control",
                "rows": 3,
                "cols": 5,
            }
        )
    )

    shop_invoice = forms.ImageField(
        allow_empty_file=False,
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    password1 = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    password2 = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone",
            "shopname",
            "address",
            "shop_invoice",
            "password1",
            "password2",
        ]

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.role = User.SELLER
        if commit:
            user.save()
        return user


class UserRegistrationForm(UserCreationForm):
    """
    Form for customer to join our platform - DawaBazaar!
    """

    username = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "Placeholder": "Steff Oberoi"}
        ),
    )

    email = forms.EmailField(
        max_length=64,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "oberois.chemist@gmail.com",
            }
        ),
    )

    password1 = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    password2 = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password1", "password2"]

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.role = "Customer"
        if commit:
            user.save()
        return user
